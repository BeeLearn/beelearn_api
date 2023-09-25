from rest_framework import serializers

from .models import (
    Choice,
    DragDropQuestion,
    MultiChoiceQuestion,
    ReorderChoice,
    ReorderChoiceQuestion,
    SingleChoiceQuestion,
    TextOptionQuestion,
)


class ChoiceSerialzier(serializers.ModelSerializer):
    """
    Choice abstract class
    """
    class Meta:
        model = Choice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question abstract class
    """


class ChoiceQuestionSerializer(QuestionSerializer):
    """
    Choice question abstract class
    """
    choices = ChoiceSerialzier(many=True)


class MultipleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    """
    MultipleChoiceQuestion model serializer
    """

    class Meta:
        model = MultiChoiceQuestion
        exclude = (
            "creator",
            "editors",
        )


class SingleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    """
    SingleChoiceQuestion model serializer
    """

    class Meta:
        model = SingleChoiceQuestion
        exclude = (
            "creator",
            "editors",
        )


class ReorderChoiceSerializer(ChoiceSerialzier):
    """
    ReorderChoice model serializer
    """

    class Meta:
        model = ReorderChoice
        fields = "__all__"


class ReorderChoiceQuestionSerializer(serializers.ModelSerializer):
    """
    ReorderChoiceQuestion model serializer
    """

    choices = ReorderChoiceSerializer(many=True)

    class Meta:
        model = ReorderChoiceQuestion
        exclude = (
            "creator",
            "editors",
        )


class DragDropQuestionSerializer(QuestionSerializer):
    """
    DragDropQuestion model serializer
    """

    class Meta:
        model = DragDropQuestion
        exclude = (
            "creator",
            "editors",
        )


class TextOptionQuestionSerializer(QuestionSerializer):
    """
    TextOptionQuestion model serializer
    """

    class Meta:
        model = TextOptionQuestion
        exclude = (
            "creator",
            "editors",
        )
