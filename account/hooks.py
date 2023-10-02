from djira.decorators import action
from djira.hooks import APIHook
from djira.observer.base_observer import Action, Scope
from djira.observer import model_observer, SignalObserver

from .models import Notification, Profile
from .serializers import NotificationSerializer, ProfileSerializer


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


class NotificationAPIHook(APIHook):
    notification_observer = model_observer(Notification)

    @notification_observer.serializer
    def notification_serializer(self, queryset: Profile, action: Action, context: dict):
        return {
            "unread": Notification.objects.filter(
                user=queryset.user,
                is_read=False,
            ).count(),
            "notification": NotificationSerializer(queryset, context=context).data,
        }

    @notification_observer.rooms
    def notification_observer_rooms(
        observer: SignalObserver, action: Action, instance: Profile, **kwargs
    ):
        yield f"notification__{instance.user.pk}"

    @notification_observer.subscribing_rooms
    def notification_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"notification__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.notification_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.notification_observer.unsubscribe(self.scope)

        await self.emit()
