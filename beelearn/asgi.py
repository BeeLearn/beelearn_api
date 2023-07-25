import os

from django.core.asgi import get_asgi_application

from reward.hooks import RewardAPIHook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beelearn.settings")

application = get_asgi_application()

from socketio import ASGIApp

from djira.consumer import Consumer
from djira.settings import jira_settings

from catalogue.hooks import LessonAPIHook, ModuleAPIHook

sio = jira_settings.SOCKET_INSTANCE

application = ASGIApp(sio, application)

consumer = Consumer(sio)

consumer.register("modules", ModuleAPIHook)
consumer.register("lessons", LessonAPIHook)
consumer.register("rewards", RewardAPIHook)

consumer.start()
