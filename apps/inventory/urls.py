"""inventory 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    InventoryTransactionViewSet,
    InventoryViewSet,
    StockCheckViewSet,
    StockTransferViewSet,
)

router = DefaultRouter()
router.register(r"inventories", InventoryViewSet, basename="inventories")
router.register(r"transactions", InventoryTransactionViewSet, basename="transactions")
router.register(r"stock-checks", StockCheckViewSet, basename="stock-checks")
router.register(r"transfers", StockTransferViewSet, basename="transfers")

urlpatterns = [
    path("", include(router.urls)),
]
