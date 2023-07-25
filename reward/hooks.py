from typing import Set
from django.db.models.signals import m2m_changed

from djira.hooks import APIHook
from djira.decorators import action
from djira.observer import observer, SignalObserver
from djira.observer.base_observer import Action, Scope


from .models import Reward


class RewardAPIHook(APIHook):
    @observer(m2m_changed, Reward.reward_unlocked_users.through)
    def reward_observer(observer: SignalObserver, action: str, **kwargs):
        match action:
            case "post_add":
                observer.dispatch(Action.UPDATE, **kwargs)

    @reward_observer.rooms
    def reward_observer_rooms(observer: SignalObserver, pk_set: Set[int], **kwargs):
        for pk in pk_set:
            yield f"reward__{pk}"

    @reward_observer.subscribing_rooms
    def reward_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"reward__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.reward_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["POST"])
    async def unsubscribe(self):
        self.reward_observer.unsubscribe(self.scope)

        await self.emit()
