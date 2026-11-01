"""master 应用序列化器。"""
from rest_framework import serializers

from .models import Category, Customer, Product, Supplier, Unit, Warehouse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "sort", "status"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "symbol"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    unit_name = serializers.CharField(source="unit.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "category",
            "category_name",
            "unit",
            "unit_name",
            "spec",
            "barcode",
            "sale_price",
            "cost_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "location", "keeper"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "contact",
            "phone",
            "level",
            "credit_limit",
            "arrears",
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "contact", "phone", "level", "payment_terms"]
