# from rest_framework.permissions import BasePermission, SAFE_METHODS
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
        print("Requesting User:", request.user)
        print("Project Contributors:", obj.contributors.all())
        print("Project Author:", obj.author)
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
    # Récupère l'objet Project associé à la vue
    project = view.project

    # Vérifie si l'utilisateur est connecté
    if not request.user.is_authenticated:
        return False  # Si l'utilisateur n'est pas connecté, retourne False

    # Vérifie si l'utilisateur est un contributeur du projet
    is_contributor = project.contributors.filter(id=request.user.id).exists()

    # Vérifie si l'utilisateur est l'auteur du projet
    is_author = project.author == request.user

    # La permission est accordée si l'utilisateur est soit un contributeur soit l'auteur du projet
    return is_contributor or is_author


class Contributor_IsAuthor(permissions.BasePermission):
    """
    Checks whether the user is the author of the project associated with the contributor.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the author of the project associated with the contributor.
        """
        # Récupère l'ID du projet à partir de l'URL de la vue
        project_id = view.kwargs.get("project_pk")

        # Vérifie si l'utilisateur est connecté et récupère son ID
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return False  # Si l'utilisateur n'est pas connecté, retourne False
        print("projet id ", project_id, " userid", user_id)

        # Vérifie si l'utilisateur est l'auteur du projet
        project = Project.objects.get(pk=project_id)
        print(project.author_id)
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
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user is a contributor or the author of the project
            project_id = request.resolver_match.kwargs.get(
                "project_pk"
            )  # Get the project ID from the view's kwargs
            # Check if the user is a contributor to the project
            project = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()
            # Check if the user is the author of the project
            project_author = Project.objects.filter(
                id=project_id, author=request.user
            ).exists()

            return (
                project or project_author
            )  # Allow access for contributors or the author of the project

        return False  # Deny access for unauthenticated users


class CanModifyOrDeleteIssue(permissions.BasePermission):
    """Customize permissions to allow only authenticated users to modify or delete issues, and authorize the issue author to perform these actions."""

    message = "You are not authorized to modify or delete this issue."

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        """

        # Check if the user is authenticated
        if request.user.is_authenticated:
            return True  # Allow access for authenticated users
        return False  # Deny access for unauthenticated users

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        """

        # Check if the user is the author of the issue
        if obj.author == request.user:
            return True  # Allow modification or deletion for the author of the issue
        return False  # Deny modification or deletion for other users


class CanCreateIssue(permissions.BasePermission):
    """
    Custom permission to allow only project contributors to create issues.
    """

    message = "You are not authorized to create an issue for this project."  # Message displayed when permission is denied

    def has_permission(self, request, view):
        """
        Check if the user has permission to create an issue for the project.

        """

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is a contributor of the project
            project_id = view.kwargs.get(
                "project_pk"
            )  # Get the project ID from the view's kwargs
            # Vérifie si l'utilisateur est l'auteur du projet
            is_author = Project.objects.filter(
                id=project_id, author=request.user
            ).exists()

            # Vérifie si l'utilisateur est un contributeur du projet
            is_contributor = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()

            return (
                is_author or is_contributor
            )  # Autorise la création de l'issue pour l'auteur du projet ou les contributeurs

        return False  # Refuse la création de l'issue pour les utilisateurs non authentifiés


class CanViewComment(permissions.BasePermission):
    """
    Permission to view comments on the issues of a project.
    Only the project author and project contributors can view comments.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has permission to view comments on the project's issues.

        """

        # Get the Project object based on the project ID in the request
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(id=project_id)

        # Check if the user is the project author or a project contributor

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
        # Vérifie si l'utilisateur est l'auteur du commentaire
        return obj.author.id == request.user.id


class CanCreateComment(permissions.BasePermission):
    """
    Permission to create a comment.
    Only project contributors can create a comment on an issue.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has permission to create a comment.

        """

        # Get the Issue object based on the issue ID in the request
        issue_id = view.kwargs.get("issue_pk")
        issue = Issue.objects.get(id=issue_id)

        # Check if the user is a contributor of the project associated with the issue
        return request.user in issue.project.contributors.all()


class AllowAnonymousAccess(permissions.BasePermission):
    """
    Permission to deny access for anonymous users.
    """

    def has_permission(self, request, view):
        """
        Check if the user is anonymous and deny access.
        """
        return False
