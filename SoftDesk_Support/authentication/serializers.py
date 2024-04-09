from rest_framework import serializers
from authentication.models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
        ]


class CustomUserDetailSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
