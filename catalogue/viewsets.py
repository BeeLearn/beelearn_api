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


class CourseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filter_fields = (
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

    filter_fields = ("lesson",)


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LikedTopicViewSet(viewsets.ModelViewSet):
    pass
