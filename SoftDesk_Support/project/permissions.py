from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to view all projects.
    """

    def has_permission(self, request, view):
        # Check if the user is an admin
        if request.user.is_staff or request.user.is_superuser:
            return True  # Allow admins to access all projects


class IsProjectCreatorOrReadOnly(BasePermission):
    """
    Custom permission to only allow the creator of the project to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the creator of the project
        return obj.author == request.user
