"""inventory 应用视图。"""
from rest_framework import viewsets

from .models import Inventory, InventoryTransaction, StockCheck, StockTransfer
from .serializers import (
    InventorySerializer,
    InventoryTransactionSerializer,
    StockCheckSerializer,
    StockTransferSerializer,
)


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """实时库存查询（只读，变更走业务单据）。"""

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filterset_fields = ["product", "warehouse"]


class InventoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """库存流水查询（只读，全量追溯）。"""

    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    filterset_fields = ["product", "warehouse", "biz_type"]


class StockCheckViewSet(viewsets.ModelViewSet):
    queryset = StockCheck.objects.all()
    serializer_class = StockCheckSerializer
    filterset_fields = ["warehouse", "status"]
    search_fields = ["check_no"]


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    filterset_fields = ["from_warehouse", "to_warehouse", "status"]
    search_fields = ["transfer_no"]
