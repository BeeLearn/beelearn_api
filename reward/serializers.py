from django.utils import timezone

from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from beelearn.mixins import ContextMixin

from account.serializers import UserSerializer

from .models import Price, Reward, Streak


class PriceSerializer(NestedModelSerializer, ContextMixin):
    """
    Price model Serializer
    """

    class Meta:
        model = Price
        fields = "__all__"


class RewardSerializer(NestedModelSerializer, ContextMixin):
    """
    Reward model Serializer
    """

    price = PriceSerializer()
    is_unlocked = serializers.SerializerMethodField()

    def get_is_unlocked(self, reward: Reward):
        return reward.reward_unlocked_users.contains(self.request.user)

    class Meta:
        model = Reward
        exclude = ["reward_unlocked_users"]


class StreakSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    """
    Streak model serializer
    """

    is_today = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    is_complete = serializers.SerializerMethodField()

    streak_complete_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )

    def get_is_expired(self, instance: Streak):
        return instance.date < timezone.localdate() and not self.get_is_complete(instance)

    def get_is_today(self, instance: Streak):
        return instance.date == timezone.localdate()

    def get_is_complete(self, instance: Streak):
        return instance.streak_complete_users.contains(self.request.user)

    class Meta:
        model = Streak
        fields = "__all__"
