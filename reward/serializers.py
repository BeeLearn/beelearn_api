from rest_framework import serializers

from beelearn.mixins import ContextMixin

from reward.models import Achievement, Price, Reward


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
        return Achievement.objects.filter(
            user=self.request.user,
            reward=reward,
        ).exists()

    class Meta:
        model = Reward
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    """
    Achievement model Serializer
    """

    class Meta:
        model = Achievement
        fields = "__all__"
