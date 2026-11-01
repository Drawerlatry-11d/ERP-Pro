"""purchase 应用序列化器。"""
from rest_framework import serializers

from .models import (
    PurchaseInbound,
    PurchaseInboundItem,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseReturn,
)


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = ["id", "product", "product_name", "qty", "price", "amount"]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, required=False)

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "order_no",
            "supplier",
            "warehouse",
            "status",
            "order_date",
            "total_amount",
            "creator",
            "remark",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PurchaseInboundItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = PurchaseInboundItem
        fields = ["id", "product", "product_name", "qty", "price", "amount"]


class PurchaseInboundSerializer(serializers.ModelSerializer):
    items = PurchaseInboundItemSerializer(many=True, required=False)

    class Meta:
        model = PurchaseInbound
        fields = [
            "id",
            "inbound_no",
            "order",
            "supplier",
            "warehouse",
            "status",
            "total_amount",
            "handler",
            "remark",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PurchaseReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturn
        fields = [
            "id",
            "return_no",
            "inbound",
            "supplier",
            "warehouse",
            "status",
            "total_amount",
            "handler",
            "remark",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
