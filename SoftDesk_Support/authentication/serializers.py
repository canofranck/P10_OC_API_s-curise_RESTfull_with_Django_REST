from rest_framework import serializers
from authentication.models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new CustomUser instance.

    This serializer is used for creating a new CustomUser instance.
    It includes fields for username, password, age, can_be_contacted,
    can_data_be_shared, and created_time.

    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        )

    def create(self, validated_data):
        """
        Create and save a new CustomUser instance.

        This method creates and saves a new CustomUser instance with the provided validated data.
        It sets the username, age, can_be_contacted, and can_data_be_shared attributes of the user,
        and sets the password using the set_password method. Finally, it saves the user to the database.

        Args:
            validated_data (dict): Validated data for creating the user instance.

        Returns:
            CustomUser: The newly created CustomUser instance.
        """
        user = CustomUser(
            username=validated_data["username"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        user.set_password(validated_data["password"])
        user.save()

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
    It includes fields for id, username, password, age, can_be_contacted,
    can_data_be_shared, and created_time.

    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        ]


class CustomUserupdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a CustomUser instance.

    This serializer is used for updating a CustomUser instance.
    It includes fields for username, password, age, can_be_contacted,
    and can_data_be_shared.

    """

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "age",
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
