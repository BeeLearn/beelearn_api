from typing import Set, Literal

from django.dispatch import receiver
from django.db.models.signals import m2m_changed



from account.models import User

from .models import Lesson, Module, Topic


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
                first_lesson = next_module.lessons.first()
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


# def _notify_mentions(
#     comment: TopicComment,
# ) -> Tuple[List[Message], List[Notification]]:
#     """
#     Notify mentions about comments
#     """
#     result: List[List[str]] = re.findall("(^|[^@\w])@(\w{3,16})", comment.content)
#     mentions = (
#         User.objects.filter(
#             username__in=[mention for _, mention in result],
#         )
#         .exclude(settings__fcm_token__isnull=True)
#         .exclude(pk=comment.user.pk)
#         .distinct()
#     )

#     parent = comment

#     if not parent.is_parent:
#         parent = TopicComment.objects.filter(
#             is_parent=True,
#             sub_topic_comments=comment,
#         ).first()
        

#     # @username tag you in a comment
#     fcm_notifications = []
#     local_notifications = []

#     for mention in mentions:
#         title = "%s mention you in a comment" % comment.user.get_full_name()
#         payload = {
#             "thread_id": str(parent.pk),
#             "topic_id": str(comment.topic.pk),
#             "sender_user_id": str(comment.user.pk),
#             "sender_username": comment.user.username,
#             "sender_full_name": comment.user.get_full_name(),
#         }

#         fcm_notifications.append(
#             build_inbox_message(
#                 title=title,
#                 body=comment.content,
#                 token=mention.settings.fcm_token,
#                 payload=payload,
#                 avatar="https://cdn.dribbble.com/users/17793/screenshots/16101765/media/beca221aaebf1d3ea7684ce067bc16e5.png",
#             )
#         )

#         local_notifications.append(
#             Notification(
#                 user=mention,
#                 title=title,
#                 body=comment.content,
#                 icon=comment.user.avatar,
#                 topic=Notification.Topic.COMMENTS,
#                 metadata=payload,
#             )
#         )

#     return fcm_notifications, local_notifications


# def _notify_commenters(
#     comment: TopicComment,
#     pk_set: Set[int],
# ) -> Tuple[List[Message], List[Notification]]:
#     """
#     Send notifications to all
#     """
#     new_sub_comments = TopicComment.objects.filter(pk__in=pk_set).exclude(
#         user=comment.user,
#     )

#     fcm_notifications = []
#     local_notifications = []

#     for new_sub_comment in new_sub_comments:
#         sub_comments = comment.sub_topic_comments.exclude(
#             pk=new_sub_comment.pk,
#             user__settings__fcm_token__isnull=True,
#         )  # .distinct("user") switch to postgres

#         # @username commented on a comment you replied
#         for sub_comment in sub_comments:
#             title = (
#                 "%s commented on a thread you replied"
#                 % sub_comment.user.get_full_name()
#             )
#             payload = {
#                 "thread_id": str(comment.pk),
#                 "topic_id": str(comment.topic.pk),
#                 "sender_user_id": new_sub_comment.pk,
#                 "sender_username": new_sub_comment.user.username,
#                 "sender_full_name": new_sub_comment.user.get_full_name(),
#             }

#             fcm_notifications.append(
#                 build_inbox_message(
#                     title=title,
#                     body=new_sub_comment.content,
#                     token=sub_comment.user.settings.fcm_token,
#                     avatar=sub_comment.user.avatar.url,
#                     payload=payload,
#                 )
#             )
#             local_notifications.append(
#                 Notification(
#                     user=sub_comment.user,
#                     title=title,
#                     body=new_sub_comment.content,
#                     icon=new_sub_comment.user.avatar.url,
#                     topic=Notification.Topic.COMMENTS,
#                     metadata=payload,
#                 )
#             )
#         # new comment on your comment
#         if new_sub_comment.user.settings.fcm_token is not None:
#             title = "%s commented on your thread" % new_sub_comment.user.get_full_name()
#             payload = {
#                 "thread_id": str(comment.pk),
#                 "topic_id": str(comment.topic.pk),
#                 "sender_user_id": new_sub_comment.pk,
#                 "sender_username": new_sub_comment.user.username,
#                 "sender_full_name": new_sub_comment.user.get_full_name(),
#             }

#             fcm_notifications.append(
#                 build_inbox_message(
#                     title=title,
#                     body=new_sub_comment.content,
#                     avatar=new_sub_comment.user.avatar.url,
#                     token=new_sub_comment.user.settings.fcm_token,
#                     payload=payload,
#                 )
#             )
#             local_notifications.append(
#                 Notification(
#                     title=title,
#                     user=new_sub_comment.user,
#                     body=new_sub_comment.content,
#                     icon=new_sub_comment.user.avatar.url,
#                     topic=Notification.Topic.COMMENTS,
#                     metadata=payload,
#                 )
#             )

#     return fcm_notifications, local_notifications


# @receiver(post_save, sender=TopicComment)
# def on_new_parent_topic_commented(instance: TopicComment, created: bool, **kwargs):
#     # if created:
#     fcm_notifications, local_notifications = _notify_mentions(instance)

#     send_all(fcm_notifications)
#     Notification.objects.bulk_create(local_notifications)


# @receiver(m2m_changed, sender=TopicComment.sub_topic_comments.through)
# def on_subtopic_commented(
#     instance: TopicComment, pk_set: Set[str], action: str, **kwargs
# ):
#     match action:
#         case "post_add":
#             # bulk send notification notifying of thread comments
#             fcm_notifications = []
#             local_notifications = []

#             mentions_fcm_notifications, mentions_local_notifications = _notify_mentions(
#                 instance
#             )
#             (
#                 commenters_fcm_notifications,
#                 commenters_local_notifications,
#             ) = _notify_commenters(
#                 instance,
#                 pk_set,
#             )

#             local_notifications += mentions_local_notifications
#             local_notifications += commenters_local_notifications

#             fcm_notifications += mentions_fcm_notifications
#             fcm_notifications += commenters_fcm_notifications

#             send_all(fcm_notifications)  # bulk send messages to devices
#             Notification.objects.bulk_create(
#                 local_notifications
#             )  # bulk create local message
