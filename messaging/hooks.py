from typing import List

from djira.scope import Scope
from djira.hooks import APIHook
from djira.decorators import action
from djira.observer.base_observer import Action
from djira.observer import model_observer, SignalObserver

from .models import Reply, Thread
from .serializers import ReplySerializer, ThreadSerializer


class ThreadAPIHook(APIHook):
    thread_observer = model_observer(Thread, ThreadSerializer)

    @thread_observer.participants
    def thread_participants(
        observer: SignalObserver,
        scopes: List[Scope],
        instance: Thread,
        **kwargs,
    ):
        return list(
            filter(lambda scope: scope.user.pk != instance.comment.user.pk, scopes)
        )

    @thread_observer.rooms
    def thread_observer_rooms(
        observer: SignalObserver,
        instance: Thread,
        **kwargs,
    ):
        yield f"thread__{instance.reference}"

    @thread_observer.subscribing_rooms
    def thread_subscribing_observer_rooms(
        observer: SignalObserver,
        scope: Scope,
    ):
        yield f"thread__{scope.query.get('reference')}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.thread_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.thread_observer.unsubscribe(self.scope)

        await self.emit()


class ReplyAPIHook(APIHook):
    reply_observer = model_observer(Reply, ReplySerializer)

    @reply_observer.participants
    def reply_observer_participants(
        observer: SignalObserver,
        scopes: List[Scope],
        instance: Reply,
        **kwargs,
    ):
        return list(
            filter(
                lambda scope: scope.user.pk != instance.comment.user.pk,
                scopes,
            )
        )

    @reply_observer.rooms
    def reply_observer_rooms(
        observer: SignalObserver,
        action: Action,
        instance: Reply,
        **kwargs,
    ):
        try:
            if instance.parent is None:
                raise StopIteration()
            yield f"reply__{instance.parent.thread.reference}"
        except Thread.DoesNotExist:
            yield f"reply__{instance.parent.pk}"

    @reply_observer.subscribing_rooms
    def reply_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"reply__{scope.query.get('thread_reference') or scope.query.get('comment_id')}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.reply_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.reply_observer.unsubscribe(self.scope)

        await self.emit()
