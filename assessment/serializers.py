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
        fields = "__all__"


class SingleChoiceQuestionSerializer(ChoiceQuestionSerializer):
    class Meta:
        model = SingleChoiceQuestion
        fields = "__all__"


class DragDropQuestionSerializer(QuestionSerializer):
    class Meta:
        model = DragDropQuestion
        fields = "__all__"


class TextOptionQuestionSerializer(QuestionSerializer):
    class Meta:
        model = TextOptionQuestion
        fields = "__all__"
