from django.db import models

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

    title = models.CharField(max_length=60)
    type = models.TextField(
        choices=QuestionType.choices,
        max_length=128,
    )

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
        max_length=128,
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
        max_length=128,
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

    question = models.TextField()
    choices = models.TextField()
    type = models.TextField(
        max_length=128,
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
        max_length=128,
        editable=False,
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.TEXT_OPTION,
    )
