from rest_framework.routers import DefaultRouter

from .viewsets import LeagueViewSet, UserLeagueViewSet

leaderboard_router = DefaultRouter()

leaderboard_router.register(r"leagues", LeagueViewSet)
leaderboard_router.register(r"user-leagues", UserLeagueViewSet)
