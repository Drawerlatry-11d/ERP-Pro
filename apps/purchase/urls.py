"""purchase 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PurchaseInboundViewSet,
    PurchaseOrderViewSet,
    PurchaseReturnViewSet,
)

router = DefaultRouter()
router.register(r"orders", PurchaseOrderViewSet, basename="purchase-orders")
router.register(r"inbounds", PurchaseInboundViewSet, basename="purchase-inbounds")
router.register(r"returns", PurchaseReturnViewSet, basename="purchase-returns")

urlpatterns = [
    path("", include(router.urls)),
]
