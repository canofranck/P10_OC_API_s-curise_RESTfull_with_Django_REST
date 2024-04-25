from rest_framework import permissions
from project.models import Project, Issue


class IsProjectContributorAuthor(permissions.BasePermission):
    """
    Permission to allow only contributors of a project to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a contributor or author of the project.
        """

        if (
            request.user in obj.contributors.all()
            or obj.author == request.user
        ):
            return True

        return False


class IsProjectAuthor(permissions.BasePermission):
    """
    Permission to allow only the author of a project to modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the author of the project.
        """
        if obj.author == request.user:
            return True
        return False


class Contributor_IsContributor(permissions.BasePermission):
    """
    Permission to allow only contributors to a project to view the list of contributors.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is a contributor of the associated project,
        or if the user is the author of the project.
        """

        project = view.project
        if not request.user.is_authenticated:
            return False

        is_contributor = project.contributors.filter(
            id=request.user.id
        ).exists()
        is_author = project.author == request.user

        return is_contributor or is_author


class Contributor_IsAuthor(permissions.BasePermission):
    """
    Checks whether the user is the author of the project associated with the contributor.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the author of the project associated with the contributor.
        """

        project_id = view.kwargs.get("project_pk")

        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return False

        project = Project.objects.get(pk=project_id)
        if project.author_id == user_id:

            return True
        return False


class CanViewIssue(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are contributors or project authors to view issues.
    """

    message = "You are not authorized to view this issue."

    def has_permission(self, request, view=None):
        """
        Check if the user has permission to view the issue.
        """

        if request.user and request.user.is_authenticated:

            project_id = request.resolver_match.kwargs.get("project_pk")
            project = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()

            project_author = Project.objects.filter(
                id=project_id, author=request.user
            ).exists()

            return (
                project or project_author
            )  # Allow access for contributors or the author of the project

        return False


class CanModifyOrDeleteIssue(permissions.BasePermission):
    """Customize permissions to allow only authenticated users to
    modify or delete issues, and authorize the issue author to perform these actions.
    """

    message = "You are not authorized to modify or delete this issue."

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        """

        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        """

        if obj.author == request.user:
            return True
        return False


class CanCreateIssue(permissions.BasePermission):
    """
    Custom permission to allow only project contributors to create issues.
    """

    message = "You are not authorized to create an issue for this project."

    def has_permission(self, request, view):
        """
        Check if the user has permission to create an issue for the project.

        """

        if request.user.is_authenticated:

            project_id = view.kwargs.get("project_pk")
            is_author = Project.objects.filter(
                id=project_id, author=request.user
            ).exists()
            is_contributor = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()

            return is_author or is_contributor

        return False


class CanViewComment(permissions.BasePermission):
    """
    Permission to view comments on the issues of a project.
    Only the project author and project contributors can view comments.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has permission to view comments on the project's issues.

        """

        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(id=project_id)

        return (
            request.user == project.author
            or request.user in project.contributors.all()
        )


class CanModifyOrDeleteComment(permissions.BasePermission):
    """
    Permission to modify or delete a comment.
    Only the comment author can modify or delete their own comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur a la permission de modifier ou supprimer un commentaire.
        """

        return obj.author.id == request.user.id


class CanCreateComment(permissions.BasePermission):
    """
    Permission to create a comment.
    Only project contributors can create a comment on an issue.
    """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            project_id = view.kwargs.get("project_pk")
            is_author = Project.objects.filter(
                id=project_id, author=request.user
            ).exists()
            is_contributor = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()

            return is_author or is_contributor
        return False


class AllowAnonymousAccess(permissions.BasePermission):
    """
    Permission to deny access for anonymous users.
    """

    def has_permission(self, request, view):
        """
        Check if the user is anonymous and deny access.
        """
        return False
