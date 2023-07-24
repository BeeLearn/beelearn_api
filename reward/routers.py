from rest_framework.routers import DefaultRouter

from reward.viewsets import AchievementViewSet, RewardViewSet, StreakViewSet

reward_router = DefaultRouter()

reward_router.register(r"rewards", RewardViewSet)
reward_router.register(r"achievements", AchievementViewSet)
reward_router.register(r"streaks", StreakViewSet)
