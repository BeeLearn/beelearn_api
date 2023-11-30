from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.parser import QueryParser
from django_restql.serializers import NestedModelSerializer

from beelearn.mixins import ContextMixin

from account.serializers import UserSerializer

from reward.serializers import PriceSerializer

from .models import League, UserLeague


class LeagueSerializer(NestedModelSerializer, ContextMixin):
    is_completed = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()

    price = PriceSerializer()

    class Meta:
        model = League
        exclude = ("users",)

    @property
    def user_league(self) -> UserLeague:
        return self.request.user.userleague

    def get_is_completed(self, league: League):
        user_league_index = League.LeagueRanking.index(self.user_league.league.type)
        league_index = League.LeagueRanking.index(league.type)

        return league_index <= user_league_index

    def get_is_unlocked(self, league: League):
        user_league_index = League.LeagueRanking.index(self.user_league.league.type)
        league_index = League.LeagueRanking.index(league.type)

        return user_league_index == league_index


class UserLeagueSerializer(NestedModelSerializer):
    user = UserSerializer(
        fields=[
            "id",
            "full_name",
            "avatar",
            "username",
            "is_premium",
        ]
    )

    class Meta:
        model = UserLeague
        exclude = ("league",)
