from rest_framework.routers import DefaultRouter

from .viewsets import EnhancementViewSet

enhancement_router = DefaultRouter()
enhancement_router.register("enhancements", EnhancementViewSet)
