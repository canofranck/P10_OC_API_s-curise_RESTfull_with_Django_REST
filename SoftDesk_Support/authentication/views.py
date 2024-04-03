from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response

from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from .permissions import IsAdminOrReadOnly


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]  # Appliquer la permission ici

    def create(self, request):
        data = request.data
        age = data.get("age")

        # Vérification de l'âge
        if age and int(age) < 15:
            return Response(
                {
                    "detail": "L'utilisateur doit avoir au moins 15 ans pour s'inscrire."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
