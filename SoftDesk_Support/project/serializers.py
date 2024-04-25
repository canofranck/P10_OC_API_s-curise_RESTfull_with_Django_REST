from rest_framework import serializers
from authentication.serializers import (
    CustomUserAuthorContributorSerializer,
)
from project.models import Project, CustomUser, Issue, Comment
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
        """
        Custom validation to check if the project already exists.
        """
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
    """
    Serializer for listing projects.
    """

    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "author",
            "contributors",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed information about a project.
    """

    author = CustomUserAuthorContributorSerializer(many=False)
    contributors = CustomUserAuthorContributorSerializer(many=True)

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
    Serializer for updating instances of Project.
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
        Method to update an instance of Project with validated data.
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
        fields = ["id", "user", "username"]

    def validate_user(self, value):
        """
        Validate the user ID provided.
        """
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
    """
    Serializer for displaying detailed information about a contributor.
    """

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
        """
        Validate the provided data for creating an issue.
        """
        assigned_to = attrs.get("assigned_to")
        project = self.context["view"].project
        if (
            assigned_to not in project.contributors.all()
            and assigned_to != project.author
        ):
            raise serializers.ValidationError(
                {
                    "assigned_to": "The assigned user must be either a contributor to the project or the project author."
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
            raise serializers.ValidationError("This issue already exists!")

        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing issues.
    """

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
    """
    Serializer for displaying detailed information about an issue.
    """

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


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a Comment
        - mandatory fields: name and description
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "description",
        ]

    def validate_name(self, value):
        """
        Validate the provided name for uniqueness.
        """
        if self.context["view"].comment.filter(name=value).exists():
            raise serializers.ValidationError(
                "This comment name exists already."
            )

        return value


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing comments.
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "name",
            "issue",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed information about a comment.
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "created_time",
            "author",
            "name",
            "description",
            "issue",
            "issue_url",
        ]
