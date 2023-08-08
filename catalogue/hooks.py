from typing import Set
from django.db.models.signals import m2m_changed

from djira.hooks import APIHook
from djira.decorators import action
from djira.observer import observer, SignalObserver
from djira.observer.base_observer import Action, Scope

from .models import Course, Lesson, Module, Topic
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    ModuleSerializer,
)


class CourseAPIHook(APIHook):
    @observer(
        m2m_changed,
        (
            Course.course_complete_users.through,
            Course.course_enrolled_users.through,
        ),
        CourseSerializer,
    )
    def course_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_add":
                observer.dispatch(Action.UPDATE, **kwargs)

    @course_observer.rooms
    def course_observer_rooms(observer: SignalObserver, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"course__{pk}"

    @course_observer.subscribing_rooms
    def course_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"course__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.course_observer.subscribe(self.scope)

        await self.emit()

    @action(methods={"POST"})
    async def unsubscribe(self):
        self.course_observer.unsubscribe(self.scope)

        await self.emit()


class ModuleAPIHook(APIHook):
    @observer(
        m2m_changed,
        (
            Module.entitled_users.through,
            Module.module_complete_users.through,
        ),
        ModuleSerializer,
    )
    def module_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_add":
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
        (
            Lesson.entitled_users.through,
            Lesson.lesson_complete_users.through,
        ),
        LessonSerializer,
    )
    def lesson_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_add":
                observer.dispatch(Action.UPDATE, **kwargs)

    @lesson_observer.rooms
    def lesson_observer_rooms(observer: SignalObserver, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"lesson__{pk}"

    @lesson_observer.subscribing_rooms
    def lesson_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"lesson__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.lesson_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["POST"])
    async def unsubscribe(self):
        self.lesson_observer.unsubscribe(self.scope)

        await self.emit()


class FavoriteAPIHook(APIHook):
    @observer(
        m2m_changed,
        Topic.likes.through,
    )
    def favourite_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_add":
                observer.dispatch(Action.UPDATE, **kwargs)
            case "post_remove":
                observer.dispatch(Action.DELETE, **kwargs)

    @favourite_observer.serializer
    def favourite_observer_serializer(
        observer: SignalObserver,
        instance: Topic,
        action: Action,
        context,
    ):
        course = Course.objects.get(module__lesson__topic=instance)

        return CourseSerializer(
            course,
            context=context,
        ).data

    @favourite_observer.rooms
    def favourite_observer_rooms(observer: SignalObserver, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"lesson__{pk}"

    @favourite_observer.subscribing_rooms
    def favourite_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"lesson__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.favourite_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["POST"])
    async def unsubscribe(self):
        self.favourite_observer.unsubscribe(self.scope)

        await self.emit()
