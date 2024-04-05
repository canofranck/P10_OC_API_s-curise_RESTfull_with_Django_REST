from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsAdminOrReadOnly, IsProjectCreatorOrReadOnly
from project.models import Project
from project.serializers import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectUpdateSerializer,
)
from rest_framework.response import Response


UserModel = get_user_model()


class ProjectViewSet(
    viewsets.ModelViewSet,
):
    serializer_class = ProjectCreateSerializer
    serializer_create_class = ProjectCreateSerializer
    serializer_detail_class = ProjectDetailSerializer
    serializer_list_class = ProjectListSerializer
    serializer_update_class = ProjectUpdateSerializer

    permission_classes = [
        IsAuthenticated,  # Autorise seulement les utilisateurs authentifiés
        IsProjectCreatorOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_list_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        elif self.action == "create":
            return self.serializer_create_class
        elif self.action == "update" or self.action == "partial_update":
            return self.serializer_update_class
        else:
            return self.serializer_class

    _project = None

    @property
    def project(self):
        if self._project is None:
            self._project = Project.objects.filter(
                contributors=self.request.user
            )

        return self._project

    def get_queryset(self):
        # use order_by to avoid the warning for the pagination
        return self.project.order_by("created_time")

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user]
        )
        author = self.request.user
        print(author)


class AdminProjectListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
