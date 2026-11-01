"""purchase 应用视图。业务校验/库存联动在开发阶段补全。"""
from rest_framework import viewsets

from .models import PurchaseInbound, PurchaseOrder, PurchaseReturn
from .serializers import (
    PurchaseInboundSerializer,
    PurchaseOrderSerializer,
    PurchaseReturnSerializer,
)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filterset_fields = ["supplier", "warehouse", "status"]
    search_fields = ["order_no", "remark"]


class PurchaseInboundViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInbound.objects.all()
    serializer_class = PurchaseInboundSerializer
    filterset_fields = ["supplier", "warehouse", "status"]
    search_fields = ["inbound_no"]


class PurchaseReturnViewSet(viewsets.ModelViewSet):
    queryset = PurchaseReturn.objects.all()
    serializer_class = PurchaseReturnSerializer
    filterset_fields = ["supplier", "warehouse", "status"]
    search_fields = ["return_no"]
