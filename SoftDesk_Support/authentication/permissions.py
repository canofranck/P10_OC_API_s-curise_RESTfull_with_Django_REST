from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to view user list.
    """

    def has_permission(self, request, view):
        # Allow GET request to user list for admins, otherwise deny access
        print(request.user.is_staff)
        print(request.user)
        if request.method == "GET":
            return request.user and request.user.is_staff
        return True
