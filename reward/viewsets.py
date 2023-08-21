from django.db.models import Case, When, Value, IntegerField
from django.utils.dateparse import parse_datetime

from rest_framework import viewsets, mixins
from rest_framework.request import Request

from beelearn.utils import get_week_start_and_end

from .models import Reward, Streak
from .serializers import RewardSerializer, StreakSerializer


class RewardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def get_queryset(self):
        entitled_rewards = Reward.objects.filter(
            reward_unlocked_users=self.request.user
        )

        queryset = self.queryset.annotate(
            is_user_entitled_to_reward=Case(
                When(id__in=entitled_rewards, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )

        return queryset.order_by("-is_user_entitled_to_reward")


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

        Streak.create_streak_for_week(start_date)

        return super().list(request)

    def get_queryset(self):
        return super().get_queryset().filter(date__range=get_week_start_and_end())
