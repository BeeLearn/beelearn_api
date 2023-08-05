from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from .models import Course, Lesson, Category, Module, Question, Topic
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    ModuleSerializer,
    QuestionSerializer,
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


class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Question
    serializer_class = QuestionSerializer


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
    def enhance(self, **kwargs):
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
        )

    @action(["GET"], detail=True)
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
        )


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
