from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

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
            return UserLeague.objects.filter(league=self.request.user.userleague.league)
        
        return UserLeague.objects.filter(user=self.request.user)
