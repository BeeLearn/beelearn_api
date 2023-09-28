from django.db.models import Case, When, Value, IntegerField
from django.utils.dateparse import parse_datetime

from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.request import Request

from beelearn.utils import get_week_start_and_end

from .models import Reward, Streak
from .serializers import RewardSerializer, StreakSerializer


class RewardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = (
        Reward.objects.select_related("price")
        .prefetch_related(
            "reward_unlocked_users",
        )
        .all()
    )
    serializer_class = RewardSerializer


class StreakViewSet(viewsets.ModelViewSet):
    queryset = Streak.objects.prefetch_related("streak_complete_users").all()
    serializer_class = StreakSerializer

    filter_fields = ("date",)

    def paginate_queryset(self, queryset):
        """
        Disable pagination on-demand
        """
        if "no_page" in self.request.query_params:
            return None

        return super().paginate_queryset(queryset)
