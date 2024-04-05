from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.models import CustomUser
from authentication.serializers import (
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserDetailSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthenticated,
    IsAdminOrOwnerOrReadOnly,
    CanCreateUser,
)

CustomUserModel = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
    serializer_create_class = CustomUserCreateSerializer
    serializer_detail_class = CustomUserDetailSerializer
    serializer_list_class = CustomUserListSerializer
    permission_classes = [
        IsAdminOrOwnerOrReadOnly,
        IsAuthenticated,
        CanCreateUser,
    ]

    def get_serializer_class(self):

        if self.action == "create":
            return self.serializer_create_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        elif self.action == "list":
            return self.serializer_list_class
        return super().get_serializer_class()

    def get_queryset(self):
        return CustomUserModel.objects.all().order_by("username")

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user]
        )
