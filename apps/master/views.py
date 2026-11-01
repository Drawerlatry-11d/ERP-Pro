"""master 应用视图：主数据 CRUD。"""
from rest_framework import viewsets

from .models import Category, Customer, Product, Supplier, Unit, Warehouse
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    ProductSerializer,
    SupplierSerializer,
    UnitSerializer,
    WarehouseSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["parent", "status"]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["category", "unit", "status"]
    search_fields = ["name", "sku", "barcode"]


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    search_fields = ["name"]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["name", "contact", "phone"]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ["name", "contact", "phone"]
