from djira.hooks import APIHook
from djira.decorators import action
from djira.observer.base_observer import Action, Scope
from djira.observer import model_observer, SignalObserver


from .models import Purchase
from .serializers import PurchaseSerializer


class PurchaseAPIHook(APIHook):
    purchase_observer = model_observer(
        Purchase,
        PurchaseSerializer,
    )

    @purchase_observer.rooms
    def purchase_observer_rooms(
        observer: SignalObserver, action: Action, instance: Purchase, **kwargs
    ):
        yield f"purchase__{instance.user.pk}"

    @purchase_observer.subscribing_rooms
    def purchase_observer_subscribing_rooms(observer: SignalObserver, scope: Scope):
        yield f"purchase__{scope.user.pk}"

    @action(methods=["POST"])
    async def subscribe(self):
        self.purchase_observer.subscribe(self.scope)

        await self.emit()

    @action(methods=["DELETE"])
    async def unsubscribe(self):
        self.purchase_observer.unsubscribe(self.scope)

        await self.emit()
