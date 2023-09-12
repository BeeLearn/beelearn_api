from django.contrib import admin

from .models import (
    Choice,
    ChoiceQuestion,
    DragDropQuestion,
    MultiChoiceQuestion,
    Question,
    ReorderChoice,
    ReorderQuestion,
    SingleChoiceQuestion,
    TextOptionQuestion,
)


class ChoiceInline(admin.StackedInline):
    model = ChoiceQuestion.choices.through
    extra = 2


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_answer")


class QuestionInline(admin.StackedInline):
    model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "title",
    )


@admin.register(MultiChoiceQuestion)
class MultipleChoiceQuestionAdmin(QuestionAdmin):
    pass


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(QuestionAdmin):
    pass


@admin.register(DragDropQuestion)
class DragDropQuestionAdmin(QuestionAdmin):
    pass


@admin.register(TextOptionQuestion)
class TextOptionQuestionAdmin(QuestionAdmin):
    pass


@admin.register(ReorderChoice)
class ReorderChoice(admin.ModelAdmin):
    pass


@admin.register(ReorderQuestion)
class ReorderQuestionAdmin(QuestionAdmin):
    pass
