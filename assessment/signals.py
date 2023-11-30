from typing import Set

from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_delete

from catalogue.models import TopicQuestion

from .models import (
    DragDropQuestion,
    MultiChoiceQuestion,
    SingleChoiceQuestion,
    ReorderChoiceQuestion,
    TextOptionQuestion,
)


Question = (
    MultiChoiceQuestion
    | SingleChoiceQuestion
    | ReorderChoiceQuestion
    | DragDropQuestion
    | TextOptionQuestion
)


@receiver(
    m2m_changed,
    sender=[
        MultiChoiceQuestion,
        SingleChoiceQuestion,
        ReorderChoiceQuestion,
        DragDropQuestion,
    ],
)
def delete_option_on_detached_from_choice(
    instance: Question, pk_sets: Set[int], **kwargs
):
    """
    delete options when removed from choice in a question
    """
    instance.choices.filter(pk__in=pk_sets).delete()


@receiver(
    post_delete,
    sender=[
        MultiChoiceQuestion,
        SingleChoiceQuestion,
        ReorderChoiceQuestion,
        DragDropQuestion,
        TextOptionQuestion,
    ],
)
def delete_topic_question_on_question_delete(instance: Question, **kwargs):
    """
    delete topic_question when topic_question.question instance is deleted
    """
    TopicQuestion.objects.filter(question=instance).delete()


@receiver(post_delete, sender=TopicQuestion)
def delete_question_when_topic_question_delete(instance: TopicQuestion, **kwargs):
    """
    delete question when topic_question instance is deleted
    """
    instance.question.delete()
