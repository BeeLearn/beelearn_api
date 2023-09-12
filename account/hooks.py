from djira.decorators import action
from djira.hooks import APIHook
from djira.observer.base_observer import Action, Scope
from djira.observer import model_observer, SignalObserver

from .models import Profile
from .serializers import ProfileSerializer


class ProfileAPIHook(APIHook):
    profile_observer = model_observer(
        Profile,
        serializer_class=ProfileSerializer,
    )

    @profile_observer.rooms
    def profile_observer_rooms(
        observer: SignalObserver, action: Action, instance: Profile, **kwargs
    ):
        yield f"profile__{instance.user.pk}"

    @profile_observer.subscribing_rooms
    def profile_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"profile__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.profile_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.profile_observer.unsubscribe(self.scope)

        await self.emit()
