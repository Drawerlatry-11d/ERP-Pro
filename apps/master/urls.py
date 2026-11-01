"""master 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CustomerViewSet,
    ProductViewSet,
    SupplierViewSet,
    UnitViewSet,
    WarehouseViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"units", UnitViewSet, basename="units")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"warehouses", WarehouseViewSet, basename="warehouses")
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"suppliers", SupplierViewSet, basename="suppliers")

urlpatterns = [
    path("", include(router.urls)),
]
