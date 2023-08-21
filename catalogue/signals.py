from typing import Set, Literal
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, m2m_changed

from .models import Lesson, Module, Topic

User = get_user_model()

Action = Literal["post_add"]


@receiver(m2m_changed, sender=Module.module_complete_users.through)
def unlock_next_module(instance: Module, action: Action, pk_set: Set[int], **kwargs):
    """
    Unlock next module when a module is marked as completed

    when all course modules are completed then course is marked as completed
    """

    match action:
        case "post_add":
            users = User.objects.filter(pk__in=pk_set)
            next_module = (
                Module.objects.filter(
                    course=instance.course,
                    created_at__gt=instance.created_at,
                )
                .order_by("created_at")
                .first()
            )

            if next_module:
                # add user as entitled to next module
                next_module.entitled_users.add(*users)
                first_lesson = next_module.lesson_set.first()
                if first_lesson:
                    first_lesson.entitled_users.add(*users)
                else:
                    # add user to those that have complete this course
                    instance.course.course_complete_users.add(*users)
            else:  # mark course as completed
                # add user to those that have complete this course
                instance.course.course_complete_users.add(*users)


@receiver(m2m_changed, sender=Lesson.lesson_complete_users.through)
def unlock_next_lesson(instance: Lesson, action: Action, pk_set: Set[int], **kwargs):
    """
    unlock next lesson when a topic is marked as completed.

    When all module lessons are completed, the `unlock_next_module` event is triggered
    """
    match action:
        case "post_add":
            users = User.objects.filter(pk__in=pk_set)
            next_lesson = (
                Lesson.objects.filter(
                    module=instance.module,
                    created_at__gt=instance.created_at,
                )
                .order_by("created_at")
                .first()
            )

            if next_lesson:
                # add user as entitled to next topic
                next_lesson.entitled_users.add(*users)
            else:  # mark topic as completed
                # add user to those that have complete module
                instance.module.module_complete_users.add(*users)


@receiver(m2m_changed, sender=Topic.topic_complete_users.through)
def unlock_next_topic(instance: Topic, action: Action, pk_set: Set[int], **kwargs):
    """
    Unlock next topic when a lesson is marked as completed.

    When all lesson topics are completed, the `unlock_next_lesson` event is triggered
    """
    match action:
        case "post_add":
            users = User.objects.filter(pk__in=pk_set)
            next_topic = Topic.objects.filter(
                lesson=instance.lesson,
                created_at__gt=instance.created_at,
            ).first()

            for user in users:
                if not instance.entitled_users.contains(user):
                    instance.entitled_users.add(user)

            if next_topic:
                # add user as entitleld to next lesson
                next_topic.entitled_users.add(*users)
            else:
                # add user to those that have complete topic
                instance.lesson.lesson_complete_users.add(*users)
