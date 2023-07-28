import os

from django.core.asgi import get_asgi_application

from reward.hooks import RewardAPIHook, StreakAPIHook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beelearn.settings")

application = get_asgi_application()

from socketio import ASGIApp

from djira.consumer import Consumer
from djira.settings import jira_settings

from catalogue.hooks import CourseAPIHook, FavoriteAPIHook, LessonAPIHook, ModuleAPIHook

sio = jira_settings.SOCKET_INSTANCE

application = ASGIApp(sio, application)

consumer = Consumer(sio)

consumer.register("courses", CourseAPIHook)
consumer.register("modules", ModuleAPIHook)
consumer.register("lessons", LessonAPIHook)
consumer.register("favourites", FavoriteAPIHook)
consumer.register("rewards", RewardAPIHook)
consumer.register("streaks", StreakAPIHook)

consumer.start()
