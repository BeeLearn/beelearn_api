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

from beelearn.mixins import ContextMixin
from beelearn.fields import ContentTypeField, GenericForeignKeyField

from messaging.models import Thread

from account.serializers import UserSerializer

from metadata.serializers import TagSerializer

from .models import Course, Lesson, Category, Module, Topic, TopicQuestion


class CourseSerializer(
    NestedModelSerializer,
    serializers.ModelSerializer,
    ContextMixin,
):
    """
    Course model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    is_new = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    liked_topic_count = serializers.SerializerMethodField()

    tags = NestedField(
        TagSerializer,
        many=True,
        required=False,
    )

    course_enrolled_users = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )

    course_complete_users = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )

    def get_liked_topic_count(self, course: Course):
        modules = course.modules.only("pk").values_list("pk")
        lessons = (
            Lesson.objects.filter(
                module__in=modules,
            )
            .only("pk")
            .values_list("pk")
        )

        return Topic.objects.filter(
            likes=self.request.user,
            lesson__in=lessons,
        ).count()

    def get_is_new(self, course: Course):
        return course.created_at > (timezone.now() - timezone.timedelta(7))

    def get_is_enrolled(self, course: Course):
        return course.course_enrolled_users.contains(self.request.user)

    def get_is_completed(self, course: Course):
        return course.course_complete_users.contains(self.request.user)

    def get_is_liked(self, course: Course):
        return (
            course.modules.filter(
                id=course.pk,
                lessons__topics__likes=self.request.user,
            )
            .distinct()
            .exists()
        )

    class Meta:
        model = Course
        exclude = ("editors",)
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class ModuleSerializer(NestedModelSerializer, ContextMixin):
    """
    Module model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
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
            "entitled_users",
            "module_complete_users",
            "editors",
        )
        extra_kwargs = {
            "course": {"write_only": True},
            "creator": {"write_only": True},
        }


class LessonSerializer(NestedModelSerializer, ContextMixin):
    """
    Lesson model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
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
            "entitled_users",
            "lesson_complete_users",
            "editors",
        )

        extra_kwargs = {
            "creators": {
                "write_only": True,
            },
            "module": {
                "write_only": True,
            },
        }


class TopicQuestionSerializer(
    NestedModelSerializer,
    ContextMixin,
):
    """
    TopicQuestion model serializer
    """

    question = GenericForeignKeyField(
        {
            DragDropQuestion: DragDropQuestionSerializer,
            TextOptionQuestion: TextOptionQuestionSerializer,
            SingleChoiceQuestion: SingleChoiceQuestionSerializer,
            MultiChoiceQuestion: MultipleChoiceQuestionSerializer,
            ReorderChoiceQuestion: ReorderChoiceQuestionSerializer,
        },
    )
    answered_users = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )
    question_content_type = ContentTypeField()
    is_answered = serializers.SerializerMethodField()

    def get_is_answered(self, question: TopicQuestion):
        return question.answered_users.contains(self.request.user)

    class Meta:
        model = TopicQuestion
        exclude = ()

        extra_kwargs = {
            "question_content_type": {
                "required": False,
                "write_only": True,
            },
            "question_id": {
                "required": False,
                "write_only": True,
            },
        }


class TopicSerializer(
    NestedModelSerializer,
    ContextMixin,
):
    """
    Topic model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    is_liked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    thread_count = serializers.SerializerMethodField()

    likes = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )
    topic_complete_users = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )
    entitled_users = NestedField(
        UserSerializer,
        many=True,
        required=False,
        write_only=True,
    )
    topic_questions = NestedField(
        TopicQuestionSerializer,
        many=True,
        required=False,
    )

    def get_is_liked(self, topic: Topic):
        return topic.likes.contains(self.request.user)

    def get_is_completed(self, topic: Topic):
        return topic.topic_complete_users.contains(self.request.user)

    def get_is_unlocked(self, topic: Topic):
        return topic.entitled_users.contains(self.request.user)

    def get_thread_count(self, topic: Topic):
        return Thread.objects.filter(reference=topic.thread_reference).count()

    class Meta:
        model = Topic
        exclude = ("editors",)

        extra_kwargs = {
            "creator": {
                "write_only": True,
            },
            "lesson": {
                "write_only": True,
            },
        }


class CategorySerializer(serializers.ModelSerializer):
    """
    Category model serializer
    """

    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        exclude = ("user",)
