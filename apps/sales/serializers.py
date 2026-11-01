"""sales 应用序列化器。"""
from rest_framework import serializers

from .models import (
    SalesOrder,
    SalesOrderItem,
    SalesOutbound,
    SalesOutboundItem,
    SalesReturn,
)


class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ["id", "product", "product_name", "qty", "price", "amount"]


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, required=False)

    class Meta:
        model = SalesOrder
        fields = [
            "id",
            "order_no",
            "customer",
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


class SalesOutboundItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = SalesOutboundItem
        fields = ["id", "product", "product_name", "qty", "price", "amount"]


class SalesOutboundSerializer(serializers.ModelSerializer):
    items = SalesOutboundItemSerializer(many=True, required=False)

    class Meta:
        model = SalesOutbound
        fields = [
            "id",
            "outbound_no",
            "order",
            "customer",
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


class SalesReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturn
        fields = [
            "id",
            "return_no",
            "outbound",
            "customer",
            "warehouse",
            "status",
            "total_amount",
            "handler",
            "remark",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
