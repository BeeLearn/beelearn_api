from django.db.models import Exists
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status

from django_restql.mixins import EagerLoadingMixin

from .models import Course, Lesson, Category, Module, Topic, TopicQuestion
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    ModuleSerializer,
    TopicQuestionSerializer,
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
        "modules",
        "course_enrolled_users",
        "course_complete_users",
    )


class ModuleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Module.objects.all().order_by("-created_at")
    serializer_class = ModuleSerializer

    filter_fields = (
        "course",
        "entitled_users",
        "module_complete_users",
    )


class LessonViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Lesson.objects.prefetch_related(
        "module",
        "entitled_users",
        "lesson_complete_users",
    ).all()
    serializer_class = LessonSerializer

    filter_fields = ("module",)


class TopicViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Topic.objects.prefetch_related(
        "likes",
        "entitled_users",
        "topic_complete_users",
        "topic_questions",
        "topic_questions__question",
        "topic_questions__answered_users",
    ).all()
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


class TopicQuestionViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = TopicQuestion.objects.all()
    serializer_class = TopicQuestionSerializer


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.prefetch_related("courses").all()
    serializer_class = CategorySerializer
