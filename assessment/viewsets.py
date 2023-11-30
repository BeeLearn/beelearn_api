from django.contrib.contenttypes.models import ContentType

from rest_framework.request import Request
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotAcceptable, NotFound

from beelearn.mixins import BulkDeleteMixin

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
    queryset = SingleChoiceQuestion.objects.all()
    serializer_classes = {
        DragDropQuestion: DragDropQuestionSerializer,
        TextOptionQuestion: TextOptionQuestionSerializer,
        SingleChoiceQuestion: SingleChoiceQuestionSerializer,
        MultiChoiceQuestion: MultipleChoiceQuestionSerializer,
        ReorderChoiceQuestion: ReorderChoiceQuestionSerializer,
    }

    content_type_field = "content_type"

    def get_queryset(self):
        return self.model_class.objects.all()

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
