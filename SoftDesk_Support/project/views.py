from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsAuthor, IsProjectAuthorOrContributor
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
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

UserModel = get_user_model()


class ProjectViewSet(
    viewsets.ModelViewSet,
):
    serializer_class = ProjectCreateSerializer
    serializer_create_class = ProjectCreateSerializer
    serializer_detail_class = ProjectDetailSerializer
    serializer_list_class = ProjectListSerializer
    serializer_update_class = ProjectUpdateSerializer

    permission_classes = [
        IsAuthenticated,  # Autorise seulement les utilisateurs authentifiés
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_list_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        elif self.action == "create":
            return self.serializer_create_class
        elif self.action == "update" or self.action == "partial_update":
            return self.serializer_update_class
        else:
            return self.serializer_class

    _project = None

    @property
    def project(self):
        if self._project is None:
            self._project = Project.objects.filter(
                contributors=self.request.user
            )

        return self._project

    def get_queryset(self):

        return self.project.order_by("created_time")

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user]
        )
        author = self.request.user
        print(author)


class AdminProjectListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    # permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContributorViewSet(ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the url
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    _project = None

    @property
    def project(self):
        """create an attribute project inside the ContributorViewSet
        this attribute is available in the view and can be called/available in the serializer
        """

        # if the view was never executed before, will make the database query
        #   otherwise _project will have a value and no database query will be performed
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.all().prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project

    def get_queryset(self):
        # use the UserModel attribute 'created-time' to order
        return self.project.contributors.all().order_by("created_time")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ContributorDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        self.project.contributors.add(serializer.validated_data["user"])

    def perform_destroy(self, instance):
        self.project.contributors.remove(instance)


class IssueViewSet(
    viewsets.ModelViewSet,
):
    """
    A simple ViewSet for creating, viewing and editing issues
    - The queryset is based on the project
    - A contributor of the project can create a new Issue and assign it to himself
        or to another contributor
    """

    serializer_class = IssueListSerializer
    serializer_create_class = IssueCreateSerializer
    serializer_detail_class = IssueDetailSerializer
    serializer_list_class = IssueListSerializer
    permission_classes = [IsProjectAuthorOrContributor, IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_list_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        elif self.action == "create":
            return self.serializer_create_class
        elif self.action == "update" or self.action == "partial_update":
            return self.serializer_detail_class
        else:
            return self.serializer_class

    _issue = None

    @property
    def issue(self):
        if self._issue is None:
            self._issue = Issue.objects.filter(
                project_id=self.kwargs["project_pk"]
            )

        return self._issue

    def get_queryset(self):
        # Obtenez la liste des contributeurs associés au projet
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        # Filtrez la liste complète des utilisateurs pour n'inclure que les contributeurs du projet
        queryset = Issue.objects.filter(project=project)
        return queryset.order_by("created_time")

    def perform_create(self, serializer):
        contributor = serializer.validated_data["assigned_to"]
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        serializer.save(
            author=self.request.user,
            assigned_to=contributor,
            project=project,
        )

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])
        self.project = project  # Définir l'attribut project dans la vue
