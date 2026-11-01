"""inventory 应用序列化器。"""
from rest_framework import serializers

from .models import (
    Inventory,
    InventoryTransaction,
    StockCheck,
    StockCheckItem,
    StockTransfer,
)


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    available_qty = serializers.DecimalField(
        max_digits=18, decimal_places=4, read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_name",
            "warehouse",
            "warehouse_name",
            "quantity",
            "locked_qty",
            "available_qty",
            "avg_cost",
            "updated_at",
        ]


class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "product",
            "product_name",
            "warehouse",
            "warehouse_name",
            "biz_type",
            "biz_no",
            "change_qty",
            "after_qty",
            "remark",
            "created_at",
        ]


class StockCheckItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = StockCheckItem
        fields = ["id", "product", "product_name", "book_qty", "actual_qty", "diff_qty", "remark"]


class StockCheckSerializer(serializers.ModelSerializer):
    items = StockCheckItemSerializer(many=True, required=False)

    class Meta:
        model = StockCheck
        fields = [
            "id",
            "check_no",
            "warehouse",
            "status",
            "handler",
            "remark",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = [
            "id",
            "transfer_no",
            "from_warehouse",
            "to_warehouse",
            "status",
            "handler",
            "remark",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
