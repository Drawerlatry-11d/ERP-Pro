"""销售域模型：销售订单、销售出库、销售退货。

对应规划文档销售域（sales_order / sales_order_item /
sales_outbound / sales_outbound_item / sales_return）。
"""
from django.db import models

from apps.common.constants import DOCUMENT_STATUS
from apps.common.models import BaseModel
from apps.master.models import Customer, Product, Warehouse
from apps.system.models import User


class SalesOrder(BaseModel):
    """销售订单（sales_order）。"""

    order_no = models.CharField("订单号", max_length=64, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="sales_orders", verbose_name="客户"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="sales_orders", verbose_name="发货仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    order_date = models.DateField("订单日期", null=True, blank=True)
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    creator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="创建人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "sales_order"
        verbose_name = "销售订单"
        verbose_name_plural = "销售订单"
        ordering = ["-id"]

    def __str__(self):
        return self.order_no


class SalesOrderItem(BaseModel):
    """销售订单明细（sales_order_item）。"""

    order = models.ForeignKey(
        SalesOrder, on_delete=models.CASCADE, related_name="items", verbose_name="订单"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="so_items", verbose_name="商品"
    )
    qty = models.DecimalField("数量", max_digits=18, decimal_places=4, default=0)
    price = models.DecimalField("单价", max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField("金额", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "sales_order_item"
        verbose_name = "销售订单明细"
        verbose_name_plural = "销售订单明细"


class SalesOutbound(BaseModel):
    """销售出库单（sales_outbound）。"""

    outbound_no = models.CharField("出库单号", max_length=64, unique=True)
    order = models.ForeignKey(
        SalesOrder, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="outbounds", verbose_name="关联销售订单"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="outbounds", verbose_name="客户"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="outbounds", verbose_name="仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "sales_outbound"
        verbose_name = "销售出库单"
        verbose_name_plural = "销售出库单"
        ordering = ["-id"]

    def __str__(self):
        return self.outbound_no


class SalesOutboundItem(BaseModel):
    """销售出库明细（sales_outbound_item）。"""

    outbound = models.ForeignKey(
        SalesOutbound, on_delete=models.CASCADE, related_name="items", verbose_name="出库单"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="outbound_items", verbose_name="商品"
    )
    qty = models.DecimalField("数量", max_digits=18, decimal_places=4, default=0)
    price = models.DecimalField("单价", max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField("金额", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "sales_outbound_item"
        verbose_name = "销售出库明细"
        verbose_name_plural = "销售出库明细"


class SalesReturn(BaseModel):
    """销售退货单（sales_return）。"""

    return_no = models.CharField("退货单号", max_length=64, unique=True)
    outbound = models.ForeignKey(
        SalesOutbound, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="returns", verbose_name="关联出库单"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="sales_returns", verbose_name="客户"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="sales_returns", verbose_name="仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "sales_return"
        verbose_name = "销售退货单"
        verbose_name_plural = "销售退货单"
        ordering = ["-id"]

    def __str__(self):
        return self.return_no
