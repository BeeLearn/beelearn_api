from rest_framework.routers import DefaultRouter


from .viewsets import ProductViewSet, PurchaseViewSet

payment_router = DefaultRouter()

payment_router.register(r"products", ProductViewSet)
payment_router.register(r"purchases", PurchaseViewSet)