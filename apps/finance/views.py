"""finance 应用视图（P1 骨架）。"""
from rest_framework import viewsets

from .models import (
    FinanceAccount,
    FinancePayable,
    FinancePayment,
    FinanceReceipt,
    FinanceReceivable,
)
from .serializers import (
    FinanceAccountSerializer,
    FinancePayableSerializer,
    FinancePaymentSerializer,
    FinanceReceiptSerializer,
    FinanceReceivableSerializer,
)


class FinanceAccountViewSet(viewsets.ModelViewSet):
    queryset = FinanceAccount.objects.all()
    serializer_class = FinanceAccountSerializer


class FinanceReceivableViewSet(viewsets.ModelViewSet):
    queryset = FinanceReceivable.objects.all()
    serializer_class = FinanceReceivableSerializer
    filterset_fields = ["customer", "status"]


class FinancePayableViewSet(viewsets.ModelViewSet):
    queryset = FinancePayable.objects.all()
    serializer_class = FinancePayableSerializer
    filterset_fields = ["supplier", "status"]


class FinanceReceiptViewSet(viewsets.ModelViewSet):
    queryset = FinanceReceipt.objects.all()
    serializer_class = FinanceReceiptSerializer
    search_fields = ["receipt_no"]


class FinancePaymentViewSet(viewsets.ModelViewSet):
    queryset = FinancePayment.objects.all()
    serializer_class = FinancePaymentSerializer
    search_fields = ["payment_no"]
