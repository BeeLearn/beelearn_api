from rest_framework.routers import DefaultRouter

from reward.viewsets import AchievementViewSet, RewardViewSet

reward_router = DefaultRouter()

reward_router.register(r"rewards", RewardViewSet)
reward_router.register(r"achievements", AchievementViewSet)
