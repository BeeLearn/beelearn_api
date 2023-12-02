from rest_framework.routers import DefaultRouter

from .viewsets import TagViewSet

metadata_router = DefaultRouter()

metadata_router.register(r"tags", TagViewSet)
