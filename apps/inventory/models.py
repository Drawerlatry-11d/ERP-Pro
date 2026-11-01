"""库存域模型（系统核心）：实时库存、库存流水、盘点、调拨。

对应规划文档库存域（inventory / inventory_transaction /
stock_check / stock_check_item / stock_transfer）。
"""
from django.db import models

from apps.common.constants import DOCUMENT_STATUS, INVENTORY_BIZ_TYPES
from apps.common.models import BaseModel
from apps.master.models import Product, Warehouse


class Inventory(BaseModel):
    """实时库存（inventory）。UNIQUE(product_id, warehouse_id)。"""

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventories", verbose_name="商品"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="inventories", verbose_name="仓库"
    )
    quantity = models.DecimalField("当前数量", max_digits=18, decimal_places=4, default=0)
    locked_qty = models.DecimalField("锁定数量", max_digits=18, decimal_places=4, default=0)
    avg_cost = models.DecimalField("移动加权平均成本", max_digits=18, decimal_places=4, default=0)

    class Meta:
        db_table = "inventory"
        verbose_name = "实时库存"
        verbose_name_plural = "实时库存"
        unique_together = (("product", "warehouse"),)

    @property
    def available_qty(self):
        """可用库存 = 当前数量 - 锁定数量。"""
        return self.quantity - self.locked_qty

    def __str__(self):
        return f"P{self.product_id}-W{self.warehouse_id}:{self.quantity}"


class InventoryTransaction(BaseModel):
    """库存流水（inventory_transaction）。全量可追溯，禁止删除。"""

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="txns", verbose_name="商品"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="txns", verbose_name="仓库"
    )
    biz_type = models.CharField("业务类型", max_length=32, choices=INVENTORY_BIZ_TYPES)
    biz_id = models.BigIntegerField("业务单ID", null=True, blank=True)
    biz_no = models.CharField("业务单号", max_length=64, blank=True, default="")
    change_qty = models.DecimalField("变动数量", max_digits=18, decimal_places=4, default=0)
    after_qty = models.DecimalField("变动后数量", max_digits=18, decimal_places=4, default=0)
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "inventory_transaction"
        verbose_name = "库存流水"
        verbose_name_plural = "库存流水"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.biz_type}:{self.change_qty}"


class StockCheck(BaseModel):
    """盘点单头（stock_check）。"""

    check_no = models.CharField("盘点单号", max_length=64, unique=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="stock_checks", verbose_name="仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    handler = models.CharField("盘点人", max_length=64, blank=True, default="")
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "stock_check"
        verbose_name = "盘点单"
        verbose_name_plural = "盘点单"
        ordering = ["-id"]

    def __str__(self):
        return self.check_no


class StockCheckItem(BaseModel):
    """盘点明细（stock_check_item）。"""

    stock_check = models.ForeignKey(
        StockCheck, on_delete=models.CASCADE, related_name="items", verbose_name="盘点单"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="check_items", verbose_name="商品"
    )
    book_qty = models.DecimalField("账面数量", max_digits=18, decimal_places=4, default=0)
    actual_qty = models.DecimalField("实盘数量", max_digits=18, decimal_places=4, default=0)
    diff_qty = models.DecimalField("差异数量", max_digits=18, decimal_places=4, default=0)
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "stock_check_item"
        verbose_name = "盘点明细"
        verbose_name_plural = "盘点明细"


class StockTransfer(BaseModel):
    """调拨单（stock_transfer）。仓库间调拨。"""

    transfer_no = models.CharField("调拨单号", max_length=64, unique=True)
    from_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="transfers_out", verbose_name="调出仓库"
    )
    to_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="transfers_in", verbose_name="调入仓库"
    )
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="DRAFT")
    handler = models.CharField("经办人", max_length=64, blank=True, default="")
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "stock_transfer"
        verbose_name = "调拨单"
        verbose_name_plural = "调拨单"
        ordering = ["-id"]

    def __str__(self):
        return self.transfer_no
