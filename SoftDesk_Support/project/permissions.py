from rest_framework.permissions import BasePermission, SAFE_METHODS
from project.models import Project, Issue


class IsProjectContributor(BasePermission):
    """
    Permission to allow only contributors of a project to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a contributor of the project.
        """

        if request.user in obj.contributors.all():
            return True
        return False


class IsProjectAuthor(BasePermission):
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


class IsProjectCreator(BasePermission):
    """
    Permission to allow only the creator of a project to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the creator of the project.
        """
        if obj.author == request.user:
            return True
        return False


class Contributor_IsContributor(BasePermission):
    """
    Permission to allow only contributors to a project to view the list of contributors.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is a contributor of the associated project.
        """
        # Retrieve the Project object associated with the view
        project = view.project
        # Check if the user is a contributor of the project
        return project.contributor_relationship.filter(
            contributor=request.user
        ).exists()


class Contributor_IsAuthor(BasePermission):
    """
    Checks whether the user is the author of the project associated with the contributor.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the author of the project associated with the contributor.
        """
        # Retrieve the project ID from the view's URL
        project_id = view.kwargs.get("project_pk")

        # Retrieve the project associated with the contributor
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False

        # Check if the user is the author of the project
        return project.author == request.user


class CanViewIssue(BasePermission):
    """
    Custom permission to allow only authenticated users who are contributors or project authors to view issues.
    """

    message = "You are not authorized to view this issue."

    def has_permission(self, request, view):
        """
        Check if the user has permission to view the issue.
        """
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is a contributor or the author of the project
            project_id = view.kwargs.get(
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
                project
                or project_author  # Allow access for contributors or the author of the project
            )
        return False  # Deny access for unauthenticated users


class CanModifyOrDeleteIssue(BasePermission):
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


class CanCreateIssue(BasePermission):
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
            project = Project.objects.filter(
                id=project_id, contributors=request.user
            ).exists()
            return (
                project  # Allow creating issue only for project contributors
            )
        return False  # Deny creating issue for unauthenticated users


class CanViewComment(BasePermission):
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


class CanModifyOrDeleteComment(BasePermission):
    """
    Permission to modify or delete a comment.
    Only the comment author can modify or delete their own comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user has permission to modify or delete a comment.

        """

        # Check if the user is the author of the comment
        return obj.author == request.user


class CanCreateComment(BasePermission):
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
