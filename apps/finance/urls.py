"""finance 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FinanceAccountViewSet,
    FinancePayableViewSet,
    FinancePaymentViewSet,
    FinanceReceiptViewSet,
    FinanceReceivableViewSet,
)

router = DefaultRouter()
router.register(r"accounts", FinanceAccountViewSet, basename="finance-accounts")
router.register(r"receivables", FinanceReceivableViewSet, basename="finance-receivables")
router.register(r"payables", FinancePayableViewSet, basename="finance-payables")
router.register(r"receipts", FinanceReceiptViewSet, basename="finance-receipts")
router.register(r"payments", FinancePaymentViewSet, basename="finance-payments")

urlpatterns = [
    path("", include(router.urls)),
]
