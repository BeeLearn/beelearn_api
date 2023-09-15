from typing import List, Optional

from django.dispatch import receiver
from django.db.models import signals

from firebase_admin.messaging import send_all


from beelearn.notification import create_inbox_message

from account.models import Notification

from .models import Comment, Reply, Thread


# todo switch to use update_fields 
# @receiver(signals.post_save, sender=Comment)
# def trigger_thread_or_reply_update_on_comment_post_save(
#     instance: Comment,
#     created: bool,
#     update_fields: List[str],
#     **kwargs,
# ):
#     """
#     trigger thread post_save  and reply post_save when comment is updated
#     """
#     if not created:
#         thread = Thread.objects.filter(comment=instance).first()

#         if thread:
#             signals.post_save.send(Thread, instance=thread, created=False)
#         else:
#             reply = Reply.objects.filter(comment=instance).first()

#             if reply:
#                 signals.post_save.send(Reply, instance=reply, created=False)


def notify(
    thread: Optional[Thread] = None,
    reply: Optional[Reply] = None,
):
    assert not (
        thread is None and reply is None
    ), "you must provide either a thread or a reply"

    messages = []
    notifications = []

    comment = thread.comment if thread else reply.comment
    mentions = comment.mentions.exclude(settings__fcm_token__isnull=True)

    payload = {
        "thread.id": str(thread.comment.pk if thread else reply.parent.pk),
        "reply.user.id": str(comment.user.pk),
        "reply.user.username": comment.user.username,
        "reply.user.avatar": comment.user.avatar.url,
        "reply.user.fullname": comment.user.get_full_name(),
    }

    debugUrl = "https://png.pngtree.com/element_our/20190529/ourmid/pngtree-black-round-pattern-user-cartoon-avatar-image_1200114.jpg"

    for mention in mentions:
        title = "%s mention you in a comment" % comment.user.get_full_name()
        body = comment.content

        messages.append(
            create_inbox_message(
                title=title,
                body=body,
                payload=payload,
                # avatar=comment.user.avatar.url,
                avatar=debugUrl,
                token=mention.settings.fcm_token,
            ),
        )
        notifications.append(
            Notification(
                user=mention,
                title=title,
                metadata=payload,
                icon=comment.user.avatar.url,
                topic=Notification.Topic.COMMENTS,
            )
        )

    if reply and reply.parent.user.settings.fcm_token is not None:
        # notify parent comment about this
        title = "%s just reply your comment" % comment.user.get_full_name()
        body = comment.content

        messages.append(
            create_inbox_message(
                title=title,
                body=body,
                payload=payload,
                # avatar=comment.user.avatar.url,
                avatar=debugUrl,
                token=reply.parent.user.settings.fcm_token,
            ),
        )
        notifications.append(
            Notification(
                user=comment.user,
                title=title,
                metadata=payload,
                icon=comment.user.avatar.url,
                topic=Notification.Topic.COMMENTS,
            ),
        )

    print(messages)
    send_all(messages)
    Notification.objects.bulk_create(notifications)


@receiver(signals.post_save, sender=Reply)
def on_reply_notify_parent_and_mentions(instance: Reply, created: bool, **kwargs):
    """
    Notify parent comment
    """
    if created:
        notify(reply=instance)


@receiver(signals.post_save, sender=Thread)
def on_thread_created_notify_mentions(instance: Thread, created: bool, **kwargs):
    """
    Notify mentions
    Todo notify thread creator followers
    """

    if created:
        notify(thread=instance)
