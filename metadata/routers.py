from rest_framework.routers import DefaultRouter

from .viewsets import TagViewSet, CategoryViewSet

metadata_router = DefaultRouter()

metadata_router.register(r"tags", TagViewSet)
metadata_router.register(r"categories", CategoryViewSet)
