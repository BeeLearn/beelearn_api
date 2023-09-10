from rest_framework import serializers


from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from payment.models import Purchase

from .models import Notification, Settings, User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    profile serializer
    """

    class Meta:
        model = Profile
        exclude = ("user",)


class SettingsSerializer(serializers.ModelSerializer):
    """
    Settings model serializer
    """

    class Meta:
        model = Settings
        exclude = ("user",)
        extra_kwargs = {"fcm_token": {"write_only": True}}


class UserSerializer(NestedModelSerializer, serializers.ModelSerializer):
    """
    User model serializer
    """

    profile = NestedField(ProfileSerializer)
    settings = NestedField(SettingsSerializer)
    is_premium = serializers.SerializerMethodField()

    def get_is_premium(self, user: User):
        return user.purchases.filter(
            user=user,
            product__is_premium=True,
            status=Purchase.Status.SUCCESSFUL,
        ).exists()

    class Meta:
        model = User
        fields = [
            "id",
            "user_type",
            "username",
            "email",
            "avatar",
            "first_name",
            "last_name",
            "profile",
            "settings",
            "is_premium",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "subscription": {"read_only": True},
        }

class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification model serializer
    """

    class Meta:
        model = Notification
        exclude = ("user",)
