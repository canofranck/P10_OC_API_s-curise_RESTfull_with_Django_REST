from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets

from project.SerializerMixin import SerializerMixin
from project.permissions import (
    IsProjectAuthor,
    IsProjectContributorAuthor,
    Contributor_IsAuthor,
    Contributor_IsContributor,
    CanViewIssue,
    CanModifyOrDeleteIssue,
    CanCreateIssue,
    CanCreateComment,
    CanViewComment,
    CanModifyOrDeleteComment,
    AllowAnonymousAccess,
)
from project.models import Project, Issue, Comment
from project.serializers import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectUpdateSerializer,
    ContributorSerializer,
    ContributorDetailSerializer,
    IssueCreateSerializer,
    IssueDetailSerializer,
    IssueListSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)
from rest_framework.response import Response

from django.conf import settings

UserModel = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    ViewSet for managing projects.
    """

    serializer_mapping = {
        "list": ProjectListSerializer,
        "retrieve": ProjectDetailSerializer,
        "create": ProjectCreateSerializer,
        "update": ProjectUpdateSerializer,
        "partial_update": ProjectUpdateSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la classe de sérialiseur appropriée en fonction de l'action de vue.

        :return: Classe de sérialiseur.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_permissions(self):
        """
        Returns the list of permissions needed for each view action.

        :return: List of permissions.
        """
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]
        elif self.action == "list" or self.action == "retrieve":
            print("je suis dans list")
            permission_classes = [IsProjectContributorAuthor]
        elif self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            print("je suis dans create")
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    _project = None

    @property
    def project(self):
        """
        Returns the project associated with the logged-in user.

        :return: Project object or None.
        """
        # avoids error if user anonymous
        if self._project is None and self.request.user.is_authenticated:
            self._project = Project.objects.filter(
                contributors=self.request.user
            )

        return self._project

    def get_queryset(self):
        """
        Returns the queryset of projects associated with the logged-in user.

        :return: Queryset of projects.
        """

        if self.project is not None:  # avoids error if user anonymous
            return self.project.order_by("created_time")
        else:
            return Project.objects.none()

    def perform_create(self, serializer):
        """
        Creates a new project.

        :param serializer: Serializer for the project.
        """
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user]
        )

    def perform_destroy(self, instance):
        """
        Deletes a contributor from the project.

        :param instance: Project instance.
        :raise ValidationError: If the user is not the author of the project.
        """
        if self.request.user == instance.author:
            instance.delete()

            return Response(
                {"message": "The project has been successfully deleted."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:

            raise ValidationError(
                "Only the author of the project can delete it."
            )


class AdminProjectListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    # permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the url

    """

    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Returns the list of permissions needed for each view action.

        :return: List of permissions.
        """
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [Contributor_IsAuthor]
        elif self.action == "list":
            permission_classes = [Contributor_IsContributor]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    _project = None

    @property
    def project(self):
        """create an attribute project inside the ContributorViewSet
        this attribute is available in the view and can be called/available in the serializer
        """

        # If the view was never executed before, it will make the database query
        # Otherwise, _project will have a value and no database query will be performed
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.all().prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project

    def get_queryset(self):
        """
        Return the queryset of contributors of the associated project, ordered by creation time.
        """
        return self.project.contributors.all().order_by("created_time")

    def get_serializer_class(self):
        """
        Return the serializer class based on the action.
        If the action is 'retrieve', use ContributorDetailSerializer, otherwise use ContributorSerializer.
        """
        if self.action == "retrieve":
            return ContributorDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        Add the validated user from the serializer data to the project's contributors.
        """
        self.project.contributors.add(serializer.validated_data["user"])

    def perform_destroy(self, instance):
        """
        Delete a contributor from the project.
        """
        if self.request.user == self.project.author:
            self.project.contributors.remove(instance)

            return Response(
                {"message": "The contributor has been successfully removed."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            raise ValidationError(
                "Only project authors can remove contributors."
            )


class IssueViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    A simple ViewSet for creating, viewing and editing issues
    - The queryset is based on the project
    - A contributor of the project can create a new Issue and assign it to himself
      or to another contributor
    """

    serializer_mapping = {
        "list": IssueListSerializer,
        "retrieve": IssueDetailSerializer,
        "create": IssueCreateSerializer,
        "update": IssueDetailSerializer,
        "partial_update": IssueDetailSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la classe de sérialiseur appropriée en fonction de l'action de vue.

        :return: Classe de sérialiseur.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_permissions(self):
        """
        Define permissions for different actions.
        """

        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [CanModifyOrDeleteIssue]
        elif self.action == "create":
            permission_classes = [CanCreateIssue]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    _issue = None

    @property
    def issue(self):
        """
        Retrieve issues related to the project.
        """
        if self._issue is None:
            self._issue = Issue.objects.filter(
                project_id=self.kwargs["project_pk"]
            )

        return self._issue

    def get_queryset(self):
        """
        Get the queryset of issues related to the project.
        """
        # Get the list of contributors associated with the project
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        # Filter the complete list of users to include only project contributors
        queryset = Issue.objects.filter(project=project)
        return queryset.order_by("created_time")

    def perform_create(self, serializer):
        """
        Create a new issue and assign it to a contributor.
        """
        contributor = serializer.validated_data["assigned_to"]
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        serializer.save(
            author=self.request.user,
            assigned_to=contributor,
            project=project,
        )

    def initial(self, request, *args, **kwargs):
        """
        Set the project attribute in the view.
        """
        super().initial(request, *args, **kwargs)
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])
        self.project = project  # Define project attribute in view


class CommentViewSet(viewsets.ModelViewSet, SerializerMixin):
    """
    A simple ViewSet for creating, viewing and editing comments
    - The queryset is based on the issue
    - Creates the issue_url
    """

    serializer_mapping = {
        "list": CommentListSerializer,
        "retrieve": CommentDetailSerializer,
        "create": CommentCreateSerializer,
        "update": CommentDetailSerializer,
        "partial_update": CommentDetailSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la classe de sérialiseur appropriée en fonction de l'action de vue.

        :return: Classe de sérialiseur.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_permissions(self):
        """
        Define permissions for different actions.
        """
        if not self.request.user.is_authenticated:
            permission_classes = [AllowAnonymousAccess]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [CanModifyOrDeleteComment]
        elif self.action in [
            "create",
        ]:
            permission_classes = [CanCreateComment]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    _comment = None

    @property
    def comment(self):
        """
        Retrieve comments related to the issue.
        """
        if self._comment is None:
            self._comment = Comment.objects.filter(
                issue_id=self.kwargs["issue_pk"]
            )

        return self._comment

    def get_queryset(self):
        """
        Get the queryset of comments related to the issue.
        """
        return self.comment.order_by("created_time")

    def perform_create(self, serializer):
        """
        Create a new comment and set issue_url.
        """
        project_pk = self.kwargs["project_pk"]
        issue_pk = self.kwargs["issue_pk"]
        issue = get_object_or_404(Issue, id=issue_pk)
        issue_url = (
            f"{settings.BASE_URL}/api/projects/{project_pk}/issues/{issue_pk}/"
        )

        serializer.save(
            author=self.request.user, issue=issue, issue_url=issue_url
        )
