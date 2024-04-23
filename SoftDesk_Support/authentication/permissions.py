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
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'administrateur ou le propriétaire de l'objet
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
        # Autoriser les administrateurs à accéder à tous les profils
        if request.user.is_staff:
            return True
        # Permettre aux utilisateurs de modifier leur propre profil
        return obj == request.user
