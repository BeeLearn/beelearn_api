from django.db import models

from martor.models import MartorField

from beelearn.models import TimestampMixin, get_revision_mixin


class Choice(models.Model):
    """
    Represent single unit of answer combination with a marker to check if its correct
    """

    name = models.TextField()
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(TimestampMixin):
    """
    Challenge questions, used to reward users on topic completion or challenges
    """

    class QuestionType(models.TextChoices):
        TEXT = (
            "TEXT",
            "Text",
        )  # simple compare text option
        DRAG_DROP = (
            "DRAG_DROP",
            "Drag Drop",
        )  # drag text options, same as text option but drag drop on ui
        TEXT_OPTION = (
            "TEXT_OPTION",
            "Text Option",
        )  # compare array of strings as option
        SINGLE_CHOICE = (
            "SINGLE_CHOICE",
            "Multiple Choice",
        )  # validate single choice from multiple options
        MULTIPLE_CHOICE = (
            "MULTIPLE_CHOICE",
            "Multiple Choice",
        )  # validate more than one choice from multiple options
        REORDER_CHOICE = (
            "REORDER_CHOICE",
            "Reorder Choice",
        )  # Rearrange choice combinations in orders

    title = MartorField()
    type = models.TextField(
        choices=QuestionType.choices,
    )

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

    def __str__(self) -> str:
        return self.title

    class Meta:
        abstract = True


class ChoiceQuestion(Question):
    choices = models.ManyToManyField(Choice)

    class Meta:
        abstract = True


class MultiChoiceQuestion(
    ChoiceQuestion,
    get_revision_mixin(
        "multi_choice_question_creator",
        "multi_choice_question_editors",
    ),
):
    """
    Multichoice question, have multiple answers and choice
    """

    type = models.TextField(
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.MULTIPLE_CHOICE,
    )


class SingleChoiceQuestion(
    ChoiceQuestion,
    get_revision_mixin(
        "single_choice_question_creator",
        "single_choice_question_editors",
    ),
):
    """
    Singlechoice question, have single answer but multiple choice
    """

    type = models.TextField(
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.SINGLE_CHOICE,
    )


class DragDropQuestion(
    Question,
    get_revision_mixin(
        "drag_drop_question_creator",
        "drag_drop_question_editors",
    ),
):
    """
    This is a text like question with drag and drop answers e.g
    ```
    # Fill in the gap, A class with name main and property score of type int with value 0.
    class %main% {
        %int% score = %0%;
    }
    ```
    We parse the question by using a special parser
    """

    question = MartorField()
    choices = models.TextField()
    type = models.TextField(
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.DRAG_DROP,
    )


class TextOptionQuestion(
    Question,
    get_revision_mixin(
        "text_option_question_creator",
        "text_option_question_editors",
    ),
):
    """
    Text editable questions
    `%int% is what type of number is called in python`
    """

    question = models.TextField()
    type = models.TextField(
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.TEXT_OPTION,
    )


class ReorderChoice(Choice):
    """
    Reorder question choice with correct position combinations
    """

    is_answer = None
    position = models.PositiveIntegerField()


class ReorderChoiceQuestion(
    Question,
    get_revision_mixin(
        "reorder_question_creator",
        "reorder_question_editors",
    ),
):
    """
    Reorder questions, reorder list for correct
    """

    choices = models.ManyToManyField(
        ReorderChoice,
    )

    type = models.TextField(
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.REORDER_CHOICE,
    )
