from rest_framework import serializers
from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
        )
