from rest_framework import serializers


from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    profile serializer
    """

    class Meta:
        model = Profile
        exclude = ("user",)


class UserSerializer(NestedModelSerializer, serializers.ModelSerializer):
    """
    User model serializer
    """

    profile = NestedField(ProfileSerializer)

    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        write_only_fields = (
            "password",
            "is_staff",
            "profile",
        )
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]
