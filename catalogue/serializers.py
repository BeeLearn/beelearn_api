from django.utils import timezone

from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from beelearn.mixins import ContextMixin

from account.serializers import UserSerializer

from .models import Course, Lesson, Category, Module, Question, Topic


class CourseSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    """
    Course model serializer
    """

    is_new = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    course_enrolled_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )

    course_complete_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )
    

    def get_is_new(self, course: Course):
        topics = Topic.objects.filter(
            lesson__module__course=course,
            created_at__gte=timezone.now() - timezone.timedelta(7),
        )
        return topics.exists()

    def get_is_enrolled(self, course: Course):
        return course.course_enrolled_users.contains(self.request.user)

    def get_is_completed(self, course: Course):
        return course.course_complete_users.contains(self.request.user)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = (
            "name",
            "content",
            "description",
            "created_at",
            "updated_at",
        )


class ModuleSerializer(serializers.ModelSerializer, ContextMixin):
    """
    Module model serializer
    """

    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_is_unlocked(self, module: Module):
        return module.entitled_users.contains(self.request.user)

    def get_is_completed(self, module: Module):
        return module.module_complete_users.contains(self.request.user)

    def get_lessons(self, module: Module):
        return LessonSerializer(
            Lesson.objects.filter(module=module),
            many=True,
            context=self.context,
        ).data

    class Meta:
        model = Module
        exclude = (
            "course",
            "entitled_users",
            "module_complete_users",
        )


class LessonSerializer(serializers.ModelSerializer, ContextMixin):
    """
    Lesson model serializer
    """

    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    def get_is_unlocked(self, lesson: Lesson):
        return lesson.entitled_users.contains(self.request.user)

    def get_is_completed(self, lesson: Lesson):
        return lesson.lesson_complete_users.contains(self.request.user)

    class Meta:
        model = Lesson
        exclude = (
            "module",
            "entitled_users",
            "lesson_complete_users",
        )


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question model serializer
    """

    class Meta:
        model = Question


class TopicSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    """
    Topic model serializer
    """

    is_liked = serializers.SerializerMethodField()
    likes = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )
    is_completed = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()

    topic_complete_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )

    class Meta:
        model = Topic
        exclude = (
            "lesson",
            "entitled_users",
        )

    def get_is_liked(self, topic: Topic):
        return topic.likes.contains(self.request.user)

    def get_is_completed(self, topic: Topic):
        return topic.topic_complete_users.contains(self.request.user)

    def get_is_unlocked(self, topic: Topic):
        return topic.entitled_users.contains(self.request.user)


class CategorySerializer(serializers.ModelSerializer):
    """
    Category model serializer
    """

    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"
