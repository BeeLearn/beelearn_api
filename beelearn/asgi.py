import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beelearn.settings")

application = get_asgi_application()

from socketio import ASGIApp

from djira.consumer import Consumer
from djira.settings import jira_settings

from messaging.hooks import ReplyAPIHook, ThreadAPIHook
from account.hooks import ProfileAPIHook, NotificationAPIHook
from catalogue.hooks import (
    CourseAPIHook,
    FavoriteAPIHook,
    LessonAPIHook,
    ModuleAPIHook,
)
from reward.hooks import RewardAPIHook, StreakAPIHook

sio = jira_settings.SOCKET_INSTANCE

application = ASGIApp(sio, application)

consumer = Consumer(sio)

consumer.register("profiles", ProfileAPIHook)
consumer.register("courses", CourseAPIHook)
consumer.register("modules", ModuleAPIHook)
consumer.register("lessons", LessonAPIHook)
consumer.register("rewards", RewardAPIHook)
consumer.register("streaks", StreakAPIHook)
consumer.register("replies", ReplyAPIHook)
consumer.register("threads", ThreadAPIHook)
consumer.register("favourites", FavoriteAPIHook)
consumer.register("notifications", NotificationAPIHook)

consumer.start()
