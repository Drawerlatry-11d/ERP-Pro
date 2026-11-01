"""finance 应用序列化器（P1 骨架）。"""
from rest_framework import serializers

from .models import (
    FinanceAccount,
    FinancePayable,
    FinancePayment,
    FinanceReceipt,
    FinanceReceivable,
)


class FinanceAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceAccount
        fields = ["id", "name", "type", "balance"]


class FinanceReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceReceivable
        fields = ["id", "customer", "amount", "remained", "due_date", "status"]


class FinancePayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancePayable
        fields = ["id", "supplier", "amount", "remained", "due_date", "status"]


class FinanceReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceReceipt
        fields = ["id", "receipt_no", "customer", "account", "amount", "handler"]


class FinancePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancePayment
        fields = ["id", "payment_no", "supplier", "account", "amount", "handler"]
