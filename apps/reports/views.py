"""报表统计视图（P1 骨架）。

报表不另建大表，基于业务表做聚合查询 + 缓存；大数据量导出走 Celery 异步。
此处先给出经营看板汇总接口骨架，二期补全利润分析、账龄等。
"""
from rest_framework import views
from rest_framework.response import Response

from apps.inventory.models import Inventory, InventoryTransaction
from apps.master.models import Product
from apps.purchase.models import PurchaseOrder
from apps.sales.models import SalesOrder


class DashboardView(views.APIView):
    """经营看板汇总。"""

    def get(self, request):
        data = {
            "product_count": Product.objects.count(),
            "inventory_sku_count": Inventory.objects.count(),
            "purchase_order_count": PurchaseOrder.objects.count(),
            "sales_order_count": SalesOrder.objects.count(),
            "stock_txn_count": InventoryTransaction.objects.count(),
            # TODO: 利润、应收应付、库存金额等汇总
        }
        return Response(data)


class PurchaseSalesSummaryView(views.APIView):
    """进销存汇总（按时间维度，二期补全）。"""

    def get(self, request):
        return Response({"message": "进销存汇总接口（二期实现）"})


class ProfitAnalysisView(views.APIView):
    """利润分析（二期实现）。"""

    def get(self, request):
        return Response({"message": "利润分析接口（二期实现）"})
