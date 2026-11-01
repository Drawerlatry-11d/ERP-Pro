"""sales 应用视图。业务校验/库存扣减在开发阶段补全。"""
from rest_framework import viewsets

from .models import SalesOrder, SalesOutbound, SalesReturn
from .serializers import (
    SalesOrderSerializer,
    SalesOutboundSerializer,
    SalesReturnSerializer,
)


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    filterset_fields = ["customer", "warehouse", "status"]
    search_fields = ["order_no", "remark"]


class SalesOutboundViewSet(viewsets.ModelViewSet):
    queryset = SalesOutbound.objects.all()
    serializer_class = SalesOutboundSerializer
    filterset_fields = ["customer", "warehouse", "status"]
    search_fields = ["outbound_no"]


class SalesReturnViewSet(viewsets.ModelViewSet):
    queryset = SalesReturn.objects.all()
    serializer_class = SalesReturnSerializer
    filterset_fields = ["customer", "warehouse", "status"]
    search_fields = ["return_no"]
