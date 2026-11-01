"""采购域模型：采购订单、采购入库、采购退货。

对应规划文档采购域（purchase_order / purchase_order_item /
purchase_inbound / purchase_inbound_item / purchase_return）。
"""
from django.db import models

from apps.common.constants import DOCUMENT_STATUS
from apps.common.models import BaseModel
from apps.master.models import Product, Supplier, Warehouse
from apps.system.models import User


class PurchaseOrder(BaseModel):
    """采购订单（purchase_order）。"""

    order_no = models.CharField("订单号", max_length=64, unique=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchase_orders", verbose_name="供应商"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="purchase_orders", verbose_name="入库仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    order_date = models.DateField("订单日期", null=True, blank=True)
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    creator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="创建人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "purchase_order"
        verbose_name = "采购订单"
        verbose_name_plural = "采购订单"
        ordering = ["-id"]

    def __str__(self):
        return self.order_no


class PurchaseOrderItem(BaseModel):
    """采购订单明细（purchase_order_item）。"""

    order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items", verbose_name="订单"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="po_items", verbose_name="商品"
    )
    qty = models.DecimalField("数量", max_digits=18, decimal_places=4, default=0)
    price = models.DecimalField("单价", max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField("金额", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "purchase_order_item"
        verbose_name = "采购订单明细"
        verbose_name_plural = "采购订单明细"


class PurchaseInbound(BaseModel):
    """采购入库单（purchase_inbound）。"""

    inbound_no = models.CharField("入库单号", max_length=64, unique=True)
    order = models.ForeignKey(
        PurchaseOrder, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="inbounds", verbose_name="关联采购订单"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="inbounds", verbose_name="供应商"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="inbounds", verbose_name="仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "purchase_inbound"
        verbose_name = "采购入库单"
        verbose_name_plural = "采购入库单"
        ordering = ["-id"]

    def __str__(self):
        return self.inbound_no


class PurchaseInboundItem(BaseModel):
    """采购入库明细（purchase_inbound_item）。"""

    inbound = models.ForeignKey(
        PurchaseInbound, on_delete=models.CASCADE, related_name="items", verbose_name="入库单"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inbound_items", verbose_name="商品"
    )
    qty = models.DecimalField("数量", max_digits=18, decimal_places=4, default=0)
    price = models.DecimalField("单价", max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField("金额", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "purchase_inbound_item"
        verbose_name = "采购入库明细"
        verbose_name_plural = "采购入库明细"


class PurchaseReturn(BaseModel):
    """采购退货单（purchase_return）。"""

    return_no = models.CharField("退货单号", max_length=64, unique=True)
    inbound = models.ForeignKey(
        PurchaseInbound, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="returns", verbose_name="关联入库单"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchase_returns", verbose_name="供应商"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="purchase_returns", verbose_name="仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    total_amount = models.DecimalField("总金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "purchase_return"
        verbose_name = "采购退货单"
        verbose_name_plural = "采购退货单"
        ordering = ["-id"]

    def __str__(self):
        return self.return_no
