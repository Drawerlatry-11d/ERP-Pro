"""sales 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SalesOrderViewSet,
    SalesOutboundViewSet,
    SalesReturnViewSet,
)

router = DefaultRouter()
router.register(r"orders", SalesOrderViewSet, basename="sales-orders")
router.register(r"outbounds", SalesOutboundViewSet, basename="sales-outbounds")
router.register(r"returns", SalesReturnViewSet, basename="sales-returns")

urlpatterns = [
    path("", include(router.urls)),
]
