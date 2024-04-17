from rest_framework.permissions import BasePermission, SAFE_METHODS
from project.models import Project


class IsProjectContributor(BasePermission):
    """
    Permission to allow only contributors of a project to access it.
    """

    def has_object_permission(self, request, view, obj):
        print("User making the request:", request.user)
        print("Contributors of the project:", obj.contributors.all())

        if request.user in obj.contributors.all():
            return True
        return False


class IsIssueContributor(BasePermission):
    """
    Permission to allow only contributors of a project to access its issues.
    """

    def has_object_permission(self, request, view, obj):
        project = obj.project
        if request.user in project.contributors.all():
            return True
        return False


class IsCommentContributor(BasePermission):
    """
    Permission to allow only contributors of a project to access its comments.
    """

    def has_object_permission(self, request, view, obj):
        project = obj.issue.project
        if request.user in project.contributors.all():
            return True
        return False


class IsProjectAuthor(BasePermission):
    """
    Permission to allow only the author of a project to modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsIssueAuthor(BasePermission):
    """
    Permission to allow only the author of an issue to modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsCommentAuthor(BasePermission):
    """
    Permission to allow only the author of a comment to modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsContributorOfAssignedIssue(BasePermission):
    """
    Permission to allow only contributors of a project to be assigned to an issue.
    """

    def has_permission(self, request, view):
        if view.kwargs.get("project_pk"):
            project = Project.objects.get(pk=view.kwargs.get("project_pk"))
            return request.user in project.contributors.all()
        return False


class IsProjectCreator(BasePermission):
    """
    Permission to allow only the creator of a project to access it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
