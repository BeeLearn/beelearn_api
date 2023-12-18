from django.db.models.query import Q

from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError

from beelearn.permissions import IsAdminOnlyAction
from beelearn.mixins import BreadCrumbListModelMixin, BulkDeleteMixin

from .models import Course, Lesson, Category, Module, Topic, TopicQuestion
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    ModuleSerializer,
    TopicQuestionSerializer,
    TopicSerializer,
)


class CourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BulkDeleteMixin,
):
    ADMIN_ONLY_ACTIONS = ["post", "delete"]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOnlyAction]

    search_fields = ("name",)
    filter_fields = (
        "modules",
        "created_at",
        "tags",
        "course_enrolled_users",
        "course_complete_users",
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return super().get_queryset().filter(Q(creator=user) | Q(editors=user))

        return super().get_queryset().exclude(is_visible=False)


class ModuleViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BulkDeleteMixin,
    BreadCrumbListModelMixin,
):
    ADMIN_ONLY_ACTIONS = ["post", "delete"]

    queryset = Module.objects.all().order_by("-created_at")
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOnlyAction]

    search_fields = ("name",)
    filter_fields = (
        "course",
        "entitled_users",
        "module_complete_users",
    )

    def get_breadcrumb(self):
        pk = self.request.query_params.get("course")

        if not pk:
            raise ValidationError({"course": ["course is required in query"]})

        course = Course.objects.get(id=pk)

        return {
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "illustration": self.request.build_absolute_uri(
                    course.illustration.url
                ),
            }
        }


class LessonViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BulkDeleteMixin,
    BreadCrumbListModelMixin,
):
    ADMIN_ONLY_ACTIONS = ["post", "delete"]

    queryset = Lesson.objects.prefetch_related(
        "module",
        "entitled_users",
        "lesson_complete_users",
    ).all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOnlyAction]

    search_fields = ("name",)
    filter_fields = ("module",)

    def get_breadcrumb(self):
        pk = self.request.query_params.get("module")

        if not pk:
            raise ValidationError({"module": ["module is required in query"]})

        module = Module.objects.prefetch_related(
            "course",
        ).get(pk=pk)
        course = module.course

        return {
            "course": {
                "id": course.id,
                "name": course.name,
            },
            "module": {
                "id": module.id,
                "name": module.name,
            },
        }


class TopicViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BulkDeleteMixin,
    BreadCrumbListModelMixin,
):
    ADMIN_ONLY_ACTIONS = ["post", "delete"]
    queryset = Topic.objects.prefetch_related(
        "likes",
        "entitled_users",
        "topic_complete_users",
        "topic_questions",
        "topic_questions__question",
        "topic_questions__answered_users",
    ).all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOnlyAction]

    search_fields = ("title",)
    filter_fields = (
        "lesson",
        "likes",
    )

    def get_breadcrumb(self):
        pk = self.request.query_params.get("lesson")

        if not pk:
            # raise ValidationError(
            #     {
            #         "lesson": ["lesson id is required in query"],
            #     },
            # )
            return None

        lesson = Lesson.objects.prefetch_related(
            "module",
            "module__course",
        ).get(id=pk)

        module = lesson.module
        course = module.course

        return {
            "course": {
                "id": course.id,
                "name": course.name,
            },
            "module": {
                "id": module.id,
                "name": module.name,
            },
            "lesson": {
                "id": lesson.id,
                "name": lesson.name,
                "is_completed": lesson.lesson_complete_users.contains(
                    self.request.user
                ),
            },
        }


class TopicQuestionViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
):
    queryset = TopicQuestion.objects.all()
    serializer_class = TopicQuestionSerializer


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.prefetch_related("courses").exclude(
        courses__isnull=True,
    )
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
