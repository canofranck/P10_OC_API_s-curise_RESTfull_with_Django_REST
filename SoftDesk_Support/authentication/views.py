from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from authentication.models import CustomUser
from authentication.serializers import (
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    CustomUserupdateSerializer,
)
from .permissions import (
    IsOwner,
    IsAdminOrOwnerOrReadOnly,
)

from project.SerializerMixin import SerializerMixin
from rest_framework.permissions import AllowAny

CustomUserModel = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet, SerializerMixin):
    queryset = CustomUser.objects.all()

    serializer_mapping = {
        "list": CustomUserListSerializer,
        "retrieve": CustomUserDetailSerializer,
        "create": CustomUserCreateSerializer,
        "update": CustomUserupdateSerializer,
        "partial_update": CustomUserupdateSerializer,
    }

    def get_serializer_class(self):
        """
        Retourne la classe de sérialiseur appropriée en fonction de l'action de vue.

        :return: Classe de sérialiseur.
        """
        return self.serializer_mapping.get(self.action, self.serializer_class)

    def get_permissions(self):

        if self.action == "retrieve":
            permission_classes = [IsOwner]
        elif self.action in [
            "list",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsAdminOrOwnerOrReadOnly]
        elif self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CustomUserModel.objects.all().order_by("id")

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user]
        )
