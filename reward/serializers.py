from django.utils import timezone

from rest_framework import serializers

from beelearn.mixins import ContextMixin

from .models import Price, Reward, Streak


class PriceSerializer(serializers.ModelSerializer, ContextMixin):
    """
    Price model Serializer
    """

    class Meta:
        model = Price
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer, ContextMixin):
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


class StreakSerializer(serializers.ModelSerializer, ContextMixin):
    """
    Streak model serializer
    """

    is_today = serializers.SerializerMethodField()
    is_complete = serializers.SerializerMethodField()

    def get_is_today(self, instance: Streak):
        return instance.date == timezone.localdate()

    def get_is_complete(self, instance: Streak):
        return instance.streak_complete_users.contains(self.request.user)

    class Meta:
        model = Streak
        fields = "__all__"
