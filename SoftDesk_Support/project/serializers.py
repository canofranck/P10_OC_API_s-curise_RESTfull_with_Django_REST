from rest_framework import serializers
from project.models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a Project
        - name, description and project_type are mandatory
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "project_type",
        ]

    def validate(self, attrs):
        if (
            self.context["view"]
            .project.filter(
                name=attrs["name"], project_type=attrs["project_type"]
            )
            .exists()
        ):
            raise serializers.ValidationError(
                "Attention! This project exists already."
            )
        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "author",
            "contributors",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "created_time",
            "name",
            "description",
            "project_type",
            "author",
            "contributors",
        ]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour les opérations de mise à jour des instances de Project.
    """

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "project_type",
        ]  # Liste des champs à mettre à jour

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour une instance de Project avec les données validées.
        """
        # Mettez en œuvre ici la logique pour mettre à jour les champs de l'instance
        # Par exemple :
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.project_type = validated_data.get(
            "project_type", instance.project_type
        )
        instance.save()
        return instance
