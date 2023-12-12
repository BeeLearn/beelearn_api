from django.db.models.query import Q
from django.contrib.contenttypes.models import ContentType

from rest_framework.request import Request
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotAcceptable, NotFound

from beelearn.mixins import BulkDeleteMixin
from beelearn.permissions import IsAdminOnlyAction

from .models import (
    SingleChoiceQuestion,
    MultiChoiceQuestion,
    ReorderChoiceQuestion,
    DragDropQuestion,
    TextOptionQuestion,
)
from .serializers import (
    SingleChoiceQuestionSerializer,
    MultipleChoiceQuestionSerializer,
    ReorderChoiceQuestionSerializer,
    DragDropQuestionSerializer,
    TextOptionQuestionSerializer,
)


class QuestionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    BulkDeleteMixin,
):
    ADMIN_ONLY_ACTIONS = ["get", "post", "patch", "delete"]

    queryset = SingleChoiceQuestion.objects.all()
    serializer_classes = {
        DragDropQuestion: DragDropQuestionSerializer,
        TextOptionQuestion: TextOptionQuestionSerializer,
        SingleChoiceQuestion: SingleChoiceQuestionSerializer,
        MultiChoiceQuestion: MultipleChoiceQuestionSerializer,
        ReorderChoiceQuestion: ReorderChoiceQuestionSerializer,
    }
    permission_classes = [IsAdminOnlyAction]

    content_type_field = "content_type"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return super().get_queryset().filter(Q(creator=user) | Q(editors=user))

        return super().get_queryset().exclude(is_visible=False)

    @property
    def model_class(self):
        request: Request = self.request
        question_type = request.query_params.get(self.content_type_field)

        if not question_type:
            raise NotAcceptable(
                {
                    self.content_type_field: [
                        "%s is required in query" % self.content_type_field
                    ]
                },
            )

        content_types = ContentType.objects.filter(model=question_type)

        if not content_types.exists():
            raise NotFound(
                {
                    self.content_type_field: [
                        "%s does not exists" % self.content_type_field
                    ]
                },
            )

        return content_types.first().model_class()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.model_class)
