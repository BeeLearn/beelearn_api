from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status

from .models import Course, Lesson, Category, Module, Topic
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    ModuleSerializer,
    TopicSerializer,
)

from enhancement.models import Enhancement
from enhancement.serializers import EnhancementSerializer


class CourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    search_fields = ("name",)
    filter_fields = (
        "module",
        "course_enrolled_users",
        "course_complete_users",
    )


class ModuleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    filter_fields = (
        "course",
        "module_complete_users",
    )


class LessonViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    filter_fields = ("module",)


class TopicViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    filter_fields = (
        "lesson",
        "likes",
    )

    @action(["POST"], detail=True)
    def enhance(self, request, **kwargs):
        """
        Enhance a topic content
        """

        topic: Topic = self.get_object()

        return Response(
            EnhancementSerializer(
                Enhancement.enhance_topic(
                    self.request.user,
                    topic,
                    Enhancement.EnhancementType.ENHANCE,
                ),
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(["POST"], detail=True)
    def summarize(self, request, **kwargs):
        """
        Summarize a topic
        """

        topic: Topic = self.get_object()

        return Response(
            EnhancementSerializer(
                Enhancement.enhance_topic(
                    self.request.user,
                    topic,
                    Enhancement.EnhancementType.SUMMARIZE,
                ),
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
