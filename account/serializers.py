from rest_framework import serializers

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    profile serializer
    """

    class Meta:
        model = Profile
        exclude = ("user",)


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    profile = ProfileSerializer()

    class Meta:
        model = User
        write_only_fields = (
            "password",
            "is_staff",
        )
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]
