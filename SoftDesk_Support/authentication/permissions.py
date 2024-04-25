from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):
    """
    Custom permission to allow only authenticated admin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the object.

    This permission checks whether the current user is the owner of the object
    or if they are a superuser. If so, permission is granted.
    """

    def has_object_permission(self, request, view, obj):

        return request.user.is_superuser or obj == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to view user list.
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user and request.user.is_staff
        return True


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to view user list.
    Users can edit their own profiles.
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj == request.user
