from rest_framework import serializers

from .models import (
    Choice,
    DragDropQuestion,
    MultiChoiceQuestion,
    SingleChoiceQuestion,
    TextOptionQuestion,
)


class ChoiceSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    pass


class ChoiceQuestionSerializer(QuestionSerializer):
    choices = ChoiceSerialzier(many=True)


class MultipleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    class Meta:
        model = MultiChoiceQuestion
        exclude = (
            "creator",
            "editors",
        )


class SingleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    class Meta:
        model = SingleChoiceQuestion
        exclude = (
            "creator",
            "editors",
        )


class DragDropQuestionSerializer(QuestionSerializer):
    class Meta:
        model = DragDropQuestion
        exclude = (
            "creator",
            "editors",
        )


class TextOptionQuestionSerializer(QuestionSerializer):
    class Meta:
        model = TextOptionQuestion
        exclude = (
            "creator",
            "editors",
        )
