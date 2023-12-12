from account.models import Notification

from .models import Reply, Thread, Comment


def down():
    Notification.objects.all().delete()
    Reply.objects.all().delete()
    Thread.objects.all().delete()
    Comment.objects.all().delete()
