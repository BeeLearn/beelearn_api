from django.db.models import F, ExpressionWrapper, IntegerField, Window
from django.db.models.functions import RowNumber, Lag, Lead


from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import LeagueSerializer, UserLeagueSerializer

from .models import League, UserLeague


class LeagueViewSet(ReadOnlyModelViewSet):
    serializer_class = LeagueSerializer
    queryset = League.objects.all()


class UserLeagueViewSet(ReadOnlyModelViewSet):
    serializer_class = UserLeagueSerializer
    queryset = UserLeague.objects.prefetch_related(
        "user",
    ).all()

    def get_queryset(self):
        if self.action == "list":
            user_league: UserLeague = self.request.user.userleague

            user_leagues = (
                self.queryset.filter(league=user_league.league)
                .annotate(
                    index=Window(
                        expression=RowNumber(),
                        order_by="xp",
                    )
                )
                .order_by("-xp")
            )

            # get user_league with index position
            user_league = user_leagues.get(user=self.request.user)

            has_same_xp = user_leagues.filter(xp=user_league.xp)

            # pick gte or equal to user
            # also pick has same xp and then other users after them
            after = user_leagues.filter(index__gte=user_league.index)[
                : has_same_xp.count() + 10
            ]

            before = set()

            if user_league.index > 10:
                # pick 1st ten
                before = user_leagues.filter(index__lte=10)
            else:
                # pick 1st 10 if user index within 1st 10
                # the pick before user
                before = user_leagues.filter(index__lt=user_league.index)

            # combine result
            # first 10 if user is amount first ten
            # (10 - user_index) + count(same_xp) + 10
            # not amount first 10
            # 10 + count(same_xp) + 10
            return list(set(after).union(before))

        return self.queryset.objects.filter(user=self.request.user)
