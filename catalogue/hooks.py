from typing import List, Set
from django.db.models.signals import m2m_changed

from djira.hooks import APIHook
from djira.decorators import action
from djira.observer import observer, model_observer, SignalObserver
from djira.observer.base_observer import Action, Scope

from .models import Course, Lesson, Module, Topic, TopicComment
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    ModuleSerializer,
    ParentTopicCommentSerializer,
    SubTopicCommentSerializer,
    TopicCommentSerializer,
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

    @action(methods={"DELETE"})
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

    @action(methods=["POST"])
    async def subscribe(self):
        self.module_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
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

    @action(methods=["DELETE"])
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

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.favourite_observer.unsubscribe(self.scope)

        await self.emit()


class TopicCommentAPIHook(APIHook):
    topic_comment_observer = model_observer(
        TopicComment,
    )

    @topic_comment_observer.participants
    def topic_comment_participants(
        observer: SignalObserver, scopes: List[Scope], instance: TopicComment, **kwargs
    ):
        return list(filter(lambda scope: scope.user.pk != instance.user.pk, scopes))

    @topic_comment_observer.serializer
    def topic_comment_serializer(
        observer: SignalObserver,
        instance: TopicComment,
        action: Action,
        context,
    ):
        if instance.is_parent:
            return ParentTopicCommentSerializer(instance, context=context).data
        # else:
        #     print("SubTopic")
        #     print(SubTopicCommentSerializer(instance, context=context).data)
        #     return SubTopicCommentSerializer(instance, context=context).data

    @topic_comment_observer.rooms
    def topic_comment_observer_rooms(
        observer: SignalObserver,
        instance: TopicComment,
        **kwargs,
    ):
        if instance.is_parent:
            yield f"topic__comment__{instance.topic.pk}"

    @topic_comment_observer.subscribing_rooms
    def topic_comment_subscribing_observer_rooms(
        observer: SignalObserver,
        scope: Scope,
    ):
        yield f"topic__comment__{scope.query.get('topicId')}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.topic_comment_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.topic_comment_observer.unsubscribe(self.scope)

        await self.emit()
