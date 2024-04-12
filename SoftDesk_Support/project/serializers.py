from rest_framework import serializers
from project.models import Project, CustomUser, Issue
from django.contrib.auth import get_user_model


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
        ]

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour une instance de Project avec les données validées.
        """

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.project_type = validated_data.get(
            "project_type", instance.project_type
        )
        instance.save()
        return instance


class ContributorSerializer(serializers.ModelSerializer):
    """
    User/Contributor Serializer
    - selected information about the User
    """

    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "user"]

    def validate_user(self, value):
        user = CustomUser.objects.filter(pk=value).first()

        if user is None:
            raise serializers.ValidationError("User does not exists!")

        if user.is_superuser:
            raise serializers.ValidationError(
                "Superusers cannot be added as contributors."
            )

        if self.context["view"].project.contributors.filter(pk=value).exists():
            raise serializers.ValidationError(
                "This user is already a contributor of this project."
            )

        return user


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]


class IssueCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create an Issue
        - mandatory fields: title, description, state, tag, priority and assigned_to
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "assigned_to",
            "title",
            "description",
            "tag",
            "status",
            "priority",
        ]

    def validate(self, attrs):
        assigned_to_id = attrs.get("assigned_to")
        print("ID de l'utilisateur assigné:", assigned_to_id)
        # Récupérer l'ID de l'utilisateur assigné
        try:
            user = CustomUser.objects.get(username=assigned_to_id)
            assigned_to_id = user.id
            print("ID de l'utilisateur  :", assigned_to_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "L'utilisateur assigné n'existe pas."
            )

        # Récupérer le projet à partir de la vue
        project = self.context["view"].project
        # Vérifier si l'utilisateur assigné est un contributeur du projet
        contributors = project.contributors.all()
        # Liste pour stocker les identifiants des contributeurs
        contributor_ids = []
        print("liste contributor", contributors)
        for contributor in contributors:
            user = CustomUser.objects.get(username=contributor)
            contributor_id = user.id
            contributor_ids.append(contributor_id)
        print("contributor_id ", contributor_ids)
        if assigned_to_id not in contributor_ids:
            raise serializers.ValidationError(
                {
                    "assigned_to_error": "L'utilisateur assigné n'est pas un contributeur du projet."
                }
            )

        if (
            self.context["view"]
            .issue.filter(
                title=attrs["title"],
                tag=attrs["tag"],
                status=attrs["status"],
                priority=attrs["priority"],
            )
            .exists()
        ):
            raise serializers.ValidationError("This issue exists already!")

        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "assigned_to",
            "title",
            "description",
            "tag",
            "status",
            "priority",
            "project",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "created_time",
            "author",
            "assigned_to",
            "title",
            "description",
            "tag",
            "status",
            "priority",
            "project",
        ]
