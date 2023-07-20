from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = User
        write_only_fields = (
            "password",
            "is_staff",
        )
