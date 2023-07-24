from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from rest_framework import viewsets, mixins
from rest_framework.request import Request

from beelearn.utils import get_week_start_and_end

from .models import Achievement, Reward, Streak
from .serializers import AchievementSerializer, RewardSerializer, StreakSerializer


class RewardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class StreakViewSet(viewsets.ModelViewSet):
    queryset = Streak.objects.all()
    serializer_class = StreakSerializer

    filter_fields = ("date",)

    def list(self, request: Request):
        """
        Create streak if not exist for the week
        """
        start_date = request.query_params.get("start_date")

        if start_date:
            start_date = parse_datetime(start_date)
            print(start_date)

        Streak.create_streak_for_week(request.user, start_date)

        return super().list(request)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                user=self.request.user,
                date__range=get_week_start_and_end(),
            )
        )
