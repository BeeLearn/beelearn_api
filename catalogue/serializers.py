from django.utils import timezone

from rest_framework import serializers

from beelearn.mixins import ContextMixin

from .models import Course, Lesson, Category, Module, Question, Topic


class CourseSerializer(serializers.ModelSerializer):
    """
    Course model serializer
    """

    is_new = serializers.SerializerMethodField()

    def get_is_new(self, course: Course):
        topics = Topic.objects.filter(
            lesson__module__course=course,
            created_at__gte=timezone.now() - timezone.timedelta(7),
        )
        return topics.exists()

    class Meta:
        model = Course
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer, ContextMixin):
    """
    Module model serializer
    """

    is_unlocked = serializers.SerializerMethodField()
    is_complete = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_is_unlocked(self, module: Module):
        return module.entitled_users.contains(self.request.user)

    def get_is_complete(self, module: Module):
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
    is_complete = serializers.SerializerMethodField()

    def get_is_unlocked(self, lesson: Lesson):
        return lesson.entitled_users.contains(self.request.user)

    def get_is_complete(self, lesson: Lesson):
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


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic model serializer
    """

    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        exclude = (
            "module",
            "entitled_users",
            "topic_complete_users",
        )


class CategorySerializer(serializers.ModelSerializer):
    """
    Category model serializer
    """

    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"
