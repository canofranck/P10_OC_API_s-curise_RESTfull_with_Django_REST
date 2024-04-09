from rest_framework import serializers
from project.models import Project, CustomUser, Issue


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
        #
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

    # create attribute 'user', which is write_only because we just need to give a value
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
        - mandatory fields: name, description, state, tag, priority and assigned_to
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
        if (
            self.context["view"]
            .issue.filter(
                name=attrs["title"],
                tag=attrs["tag"],
                state=attrs["status"],
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
