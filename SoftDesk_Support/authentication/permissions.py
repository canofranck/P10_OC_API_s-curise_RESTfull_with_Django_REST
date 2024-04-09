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


class IsAuthenticated(BasePermission):
    """
    Custom permission to allow only authenticated users.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True  # Autoriser les requêtes POST sans authentification
        return bool(request.user and request.user.is_authenticated)


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
        # Autoriser les administrateurs à accéder à tous les profils
        if request.user.is_staff:
            return True
        # Permettre aux utilisateurs de modifier leur propre profil
        return obj == request.user
