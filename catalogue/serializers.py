from django.utils.timezone import timedelta, now

from rest_framework import serializers

from account.models import UserCourse

from .models import Course, Lesson, Category, Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question model serializer
    """

    class Meta:
        model = Question


class LessonSerializer(serializers.ModelSerializer):
    """
    Lesson model serializer
    """

    is_liked = serializers.SerializerMethodField("_is_liked")

    class Meta:
        model = Lesson
        exclude = (
            "course",
            "likes",
        )

    def _is_liked(self, lesson: Lesson) -> bool:
        """
        Check if current authenticated user like this lesson
        """

        user = self.context.get("request").user

        return lesson.likes.contains(user)


class CourseSerializer(serializers.ModelSerializer):
    """
    Course model serializer
    """

    is_new = serializers.SerializerMethodField("_is_new")
    last_lesson = serializers.SerializerMethodField("_last_lesson")

    def _last_lesson(self, course: Course):
        try:
            last_lesson = UserCourse.objects.get(course=course).last_lesson
            return LessonSerializer(last_lesson).data
        except UserCourse.DoesNotExist:
            return None

    def _is_new(self, course: Course):
        lessons = Lesson.objects.filter(
            course=course,
            created_at__gte=now() - timedelta(7),
        )
        return lessons.exists()

    class Meta:
        model = Course
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Category model serializer
    """

    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"
