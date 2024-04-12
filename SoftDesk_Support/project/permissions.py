from rest_framework.permissions import BasePermission, SAFE_METHODS
from project.models import Project


class IsAuthor(BasePermission):
    """
    Object-level permission to only allow obj.authors to edit and delete an object
    """

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectAuthorOrContributor(BasePermission):
    """
    Object-level permission to only allow authors to edit and delete an object
    - special permission for the ContributorViewSet
    """

    message = "You have to be the author to read , update or delete."

    def has_permission(self, request, view):
        # GET and POST
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        # check if the request.user is a contributor
        if request.user in project.contributors.all():
            return True

    def has_object_permission(self, request, view, obj):
        # GET, POST, PUT, PATCH, DELETE with pk
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)
        return project.author == request.user


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return True  # Allow all requests to pass the initial permission check

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action in ["retrieve", "update", "partial_update"]:
            return (
                obj == request.user
            )  # Allow the user to retrieve, update or partial_update their own data
        else:
            return False  # For other actions, deny all requests
