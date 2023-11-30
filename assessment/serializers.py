from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from .models import (
    Choice,
    Option,
    DragDropQuestion,
    MultiChoiceQuestion,
    ReorderOption,
    ReorderChoiceQuestion,
    SingleChoiceQuestion,
    TextOptionQuestion,
)


class OptionSerialzer(NestedModelSerializer):
    """
    Choice abstract class
    """

    class Meta:
        model = Option
        fields = "__all__"


class QuestionSerializer(NestedModelSerializer):
    """
    Question abstract class
    """

    content_type = serializers.SerializerMethodField()

    def get_content_type(
        self,
        instance: SingleChoiceQuestion
        | MultiChoiceQuestion
        | DragDropQuestion
        | TextOptionQuestion
        | ReorderChoiceQuestion,
    ):
        return instance._meta.model_name


class ChoiceQuestionSerializer(QuestionSerializer):
    """
    Choice question abstract class
    """

    choices = NestedField(OptionSerialzer, many=True)


class MultipleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    """
    MultipleChoiceQuestion model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )

    class Meta:
        model = MultiChoiceQuestion
        exclude = ("editors",)


class SingleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    """
    SingleChoiceQuestion model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )

    class Meta:
        model = SingleChoiceQuestion
        exclude = ("editors",)


class ReorderOptionSerializer(NestedModelSerializer):
    """
    ReorderChoice model serializer
    """

    class Meta:
        model = ReorderOption
        fields = "__all__"


class ReorderChoiceQuestionSerializer(QuestionSerializer):
    """
    ReorderChoiceQuestion model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )
    choices = NestedField(
        ReorderOptionSerializer,
        many=True,
    )

    class Meta:
        model = ReorderChoiceQuestion
        exclude = ("editors",)

class ChoiceSerializer(NestedModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"

class DragDropQuestionSerializer(QuestionSerializer):
    """
    DragDropQuestion model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )

    choices = NestedField(ChoiceSerializer, many=True)

    class Meta:
        model = DragDropQuestion
        exclude = ("editors",)


class TextOptionQuestionSerializer(QuestionSerializer):
    """
    TextOptionQuestion model serializer
    """

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )

    class Meta:
        model = TextOptionQuestion
        exclude = ("editors",)
