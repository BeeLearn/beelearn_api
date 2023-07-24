from rest_framework.response import Response
from rest_framework.request import Request
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


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def list(self, request: Request):
        courses = Course.objects.filter(
            module__lesson__topic__likes=request.user
        ).distinct()
        print(courses)

        return Response(
            list(
                map(
                    lambda course: {
                        "course": CourseSerializer(
                            course,
                            context=self.get_serializer_context(),
                        ).data,
                        "topics": TopicSerializer(
                            Topic.objects.filter(
                                likes=request.user,
                                lesson__module__course=course,
                            ),
                            many=True,
                            context=self.get_serializer_context(),
                        ).data,
                    },
                    courses,
                ),
            ),
        )
