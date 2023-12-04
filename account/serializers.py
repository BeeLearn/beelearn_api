from rest_framework import serializers
from rest_framework.authtoken.models import Token


from django_restql.mixins import DynamicFieldsMixin
from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from payment.models import Purchase

from .models import Notification, Settings, User, Profile

from metadata.serializers import CategorySerializer


class ProfileSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    profile serializer
    """

    class Meta:
        model = Profile
        exclude = ("user",)


class SettingsSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Settings model serializer
    """

    class Meta:
        model = Settings
        exclude = ("user",)
        extra_kwargs = {"fcm_token": {"write_only": True}}


class TokenSerializer(serializers.ModelSerializer):
    """
    Token model serializer
    """

    class Meta:
        model = Token
        fields = ("key",)


class UserSerializer(DynamicFieldsMixin, NestedModelSerializer):
    """
    User model serializer
    """
    profile = NestedField(ProfileSerializer)
    settings = NestedField(SettingsSerializer)

    token = serializers.SerializerMethodField()
    full_name= serializers.SerializerMethodField()
    is_premium = serializers.SerializerMethodField()
    unread_notifications = serializers.SerializerMethodField()

    categories = NestedField(CategorySerializer, many=True)

    def get_full_name(self, user: User):
        return user.get_full_name()
    
    def get_token(self, user: User):
        return TokenSerializer(
            Token.objects.get(user=user),
            read_only=True,
        ).data

    def get_is_premium(self, user: User):
        return user.purchases.filter(
            user=user,
            product__consumable=False,
            status=Purchase.Status.SUCCESSFUL,
        ).exists()

    def get_unread_notifications(self, user: User):
        return user.notifications.filter(
            user=user,
            is_read=False,
        ).count()

    class Meta:
        model = User
        exclude = (
            "user_permissions",
            "groups",
            "last_login",
            "is_active",
        )
        extra_kwargs = {
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "password": {"write_only": True},
            "subscription": {"read_only": True},
        }


class NotificationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Notification model serializer
    """

    class Meta:
        model = Notification
        exclude = ("user",)
