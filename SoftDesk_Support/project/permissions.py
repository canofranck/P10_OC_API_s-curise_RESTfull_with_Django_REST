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
    Object-level permission to only allow authors or contributors to edit and delete an object
    """

    message = (
        "You have to be the author or a contributor to read, update or delete."
    )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        # Check if the request.user is the author of the project
        if project.author == request.user:
            return True

        # Check if the request.user is a contributor to the project
        if request.user in project.contributors.all():
            return True

        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_pk")

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False

        # Vérifier si l'utilisateur est l'auteur du projet
        if project.author == request.user:
            return True

        # Vérifier si l'utilisateur est un contributeur au projet
        if request.user in project.contributors.all():
            return True

        return False


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


class ProjectPermissions(BasePermission):
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs["project_pk"])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(
                    contributors__user=request.user
                )
            return request.user == project.author
        except KeyError:
            return True
