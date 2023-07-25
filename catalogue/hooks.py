from typing import Set
from django.db.models.signals import m2m_changed

from djira.hooks import APIHook
from djira.decorators import action
from djira.observer import observer, SignalObserver
from djira.observer.base_observer import Action, Scope

from .models import Lesson, Module
from .serializers import LessonSerializer, ModuleSerializer


class ModuleAPIHook(APIHook):
    @observer(
        m2m_changed,
        Module.entitled_users.through,
        ModuleSerializer,
    )
    def module_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_save":
                observer.dispatch(Action.UPDATE, **kwargs)

    @module_observer.rooms
    def module_rooms(observer, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"module__{pk}"

    @module_observer.subscribing_rooms
    def module_rooms(observer, scope: Scope):
        yield f"module__{scope.user.pk}"

    @action(methods=["SUBSCRIPTION"])
    async def subscribe(self):
        self.module_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["POST"])
    async def unsubscribe(self):
        self.module_observer.unsubscribe(self.scope)

        await self.emit()


class LessonAPIHook(APIHook):
    @observer(
        m2m_changed,
        Lesson.entitled_users.through,
        LessonSerializer,
    )
    def lesson_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_save":
                observer.dispatch(Action.UPDATE, **kwargs)

    @lesson_observer.rooms
    def lesson_rooms(observer, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"lesson__{pk}"

    @lesson_observer.subscribing_rooms
    def lesson_rooms(observer, scope: Scope):
        yield f"lesson__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.lesson_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["POST"])
    async def unsubscribe(self):
        self.lesson_observer.unsubscribe(self.scope)

        await self.emit()
