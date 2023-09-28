from django.utils import timezone

from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer
from assessment.models import (
    DragDropQuestion,
    MultiChoiceQuestion,
    ReorderChoiceQuestion,
    SingleChoiceQuestion,
    TextOptionQuestion,
)
from assessment.serializers import (
    DragDropQuestionSerializer,
    MultipleChoiceQuestionSerializer,
    ReorderChoiceQuestionSerializer,
    SingleChoiceQuestionSerializer,
    TextOptionQuestionSerializer,
)

from generic_relations.relations import GenericRelatedField

from beelearn.mixins import ContextMixin

from account.serializers import UserSerializer

from .models import Course, Lesson, Category, Module, Topic, TopicQuestion


class CourseSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    """
    Course model serializer
    """

    is_new = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
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
        return course.created_at > (timezone.now() - timezone.timedelta(7))

    def get_is_enrolled(self, course: Course):
        return course.course_enrolled_users.contains(self.request.user)

    def get_is_completed(self, course: Course):
        return course.course_complete_users.contains(self.request.user)

    def get_is_liked(self, course: Course):
        return (
            Course.objects.filter(
                id=course.pk,
                module__lessons__topic__likes=self.request.user,
            )
            .distinct()
            .exists()
        )

    class Meta:
        model = Course
        exclude = (
            "editors",
            "creator",
        )
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
            module.lessons.order_by("created_at"),
            many=True,
            context=self.context,
        ).data

    class Meta:
        model = Module
        exclude = (
            "course",
            "entitled_users",
            "module_complete_users",
            "editors",
            "creator",
        )


class LessonSerializer(NestedModelSerializer, ContextMixin):
    """
    Lesson model serializer
    """

    module_id = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    def get_module_id(self, lesson: Lesson):
        return lesson.module.pk

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
            "creator",
            "editors",
        )


class TopicQuestionSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    question = GenericRelatedField(
        {
            DragDropQuestion: DragDropQuestionSerializer(),
            TextOptionQuestion: TextOptionQuestionSerializer(),
            SingleChoiceQuestion: SingleChoiceQuestionSerializer(),
            MultiChoiceQuestion: MultipleChoiceQuestionSerializer(),
            ReorderChoiceQuestion: ReorderChoiceQuestionSerializer(),
        }
    )
    answered_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )
    is_answered = serializers.SerializerMethodField()

    def get_is_answered(self, question: TopicQuestion):
        return question.answered_users.contains(self.request.user)

    class Meta:
        model = TopicQuestion
        exclude = (
            "question_id",
            "question_content_type",
        )
        extra_kwargs = {
            "topic": {
                "read_only": True,
            }
        }


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
    topic_questions = serializers.SerializerMethodField()

    topic_complete_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )

    entitled_users = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
    )

    class Meta:
        model = Topic
        exclude = (
            "lesson",
            "creator",
            "editors",
        )

    def get_is_liked(self, topic: Topic):
        return topic.likes.contains(self.request.user)

    def get_is_completed(self, topic: Topic):
        return topic.topic_complete_users.contains(self.request.user)

    def get_is_unlocked(self, topic: Topic):
        return topic.entitled_users.contains(self.request.user)

    def get_topic_questions(self, topic: Topic):
        return TopicQuestionSerializer(
            topic.topic_questions,
            many=True,
            context=self.context,
        ).data


class CategorySerializer(serializers.ModelSerializer):
    """
    Category model serializer
    """

    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        exclude = (
            "creator",
            "editors",
        )
