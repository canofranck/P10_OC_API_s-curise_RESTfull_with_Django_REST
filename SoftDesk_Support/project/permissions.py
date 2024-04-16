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

        if request.user.is_authenticated:
            return True  # Autoriser les utilisateurs authentifiés à créer un nouveau projet
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Vérifier si l'utilisateur est l'auteur du projet
        return obj.author == request.user


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
