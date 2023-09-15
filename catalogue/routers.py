from rest_framework.routers import DefaultRouter

from .viewsets import (
    CourseViewSet,
    LessonViewSet,
    CategoryViewSet,
    ModuleViewSet,
    TopicViewSet,
)

catalogue_router = DefaultRouter()

catalogue_router.register(r"courses", CourseViewSet)
catalogue_router.register(r"modules", ModuleViewSet)
catalogue_router.register(r"lessons", LessonViewSet)
catalogue_router.register(r"topics", TopicViewSet)
catalogue_router.register(r"categories", CategoryViewSet)
