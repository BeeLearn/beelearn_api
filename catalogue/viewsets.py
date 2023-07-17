from rest_framework import viewsets, mixins

from .models import Course, Lesson, Category, Question
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    QuestionSerializer,
)


class QuestionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Question
    serializer_class = QuestionSerializer


class LessonViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    filter_fields = ("course",)


class CourseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
