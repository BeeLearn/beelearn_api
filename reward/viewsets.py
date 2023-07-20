from rest_framework import viewsets, mixins

from reward.models import Achievement, Reward
from reward.serializers import AchievementSerializer, RewardSerializer


class RewardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
