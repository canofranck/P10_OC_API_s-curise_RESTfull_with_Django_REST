from rest_framework import serializers
from authentication.models import CustomUser
from datetime import datetime
from django.utils import timezone


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new CustomUser instance.

    This serializer is used for creating a new CustomUser instance.
    It includes fields for username, password, date, can_be_contacted,
    can_data_be_shared, and created_time.

    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        )

    def create(self, validated_data):
        """
        Create and save a new CustomUser instance.

        This method creates and saves a new CustomUser instance with the provided validated data.
        It sets the username, date, can_be_contacted, and can_data_be_shared attributes of the user,
        and sets the password using the set_password method. Finally, it saves the user to the database.

        Args:
            validated_data (dict): Validated data for creating the user instance.

        Returns:
            CustomUser: The newly created CustomUser instance.
        """

        date_of_birth = validated_data.get("date_of_birth")

        if date_of_birth:
            today = timezone.now().date()
            age = (
                today.year
                - date_of_birth.year
                - (
                    (today.month, today.day)
                    < (date_of_birth.month, date_of_birth.day)
                )
            )
            if age < 15:
                raise serializers.ValidationError(
                    "L'utilisateur doit avoir au moins 15 ans."
                )

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            date_of_birth=date_of_birth,
            can_be_contacted=validated_data.get("can_be_contacted", False),
            can_data_be_shared=validated_data.get("can_data_be_shared", False),
        )

        return user


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing CustomUser instances.

    This serializer is used for listing CustomUser instances.
    It includes fields for id, username, and password.

    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
        ]


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving detailed information about a CustomUser instance.

    This serializer is used for retrieving detailed information about a CustomUser instance.
    It includes fields for id, username, password, date, can_be_contacted,
    can_data_be_shared, and created_time.

    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        ]


class CustomUserupdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a CustomUser instance.

    This serializer is used for updating a CustomUser instance.
    It includes fields for username, password, date, can_be_contacted,
    and can_data_be_shared.

    """

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        ]


class CustomUserAuthorContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for listing CustomUser instances as authors or contributors.

    This serializer is used for listing CustomUser instances as authors or contributors.
    It includes fields for id and username.

    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
        ]
