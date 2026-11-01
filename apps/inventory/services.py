"""库存变更服务：事务 + 行锁 + 流水表（三件套）。

这是库存一致性的核心。所有库存变动（入库/出库/退货/盘点/调拨）都必须
经过本服务，禁止在视图里直接改 Inventory.quantity。

设计要点：
1. 在数据库事务内操作，任一环节失败整体回滚；
2. 对 Inventory 行加 `SELECT ... FOR UPDATE` 行锁，避免并发超卖；
3. 每次变动写入 InventoryTransaction 流水，保证全量可追溯；
4. 出库/退货前校验可用库存，不足则抛异常。
"""
from decimal import Decimal

from django.db import transaction
from django.db.models import F

from apps.common.constants import (
    PURCHASE_IN,
    PURCHASE_RETURN,
    SALES_OUT,
    SALES_RETURN,
    STOCK_CHECK,
    STOCK_TRANSFER,
)
from .models import Inventory, InventoryTransaction


def _get_or_create_locked(product_id, warehouse_id):
    """获取（并加行锁）指定 商品+仓库 的库存行。"""
    inv, _created = Inventory.objects.get_or_create(
        product_id=product_id,
        warehouse_id=warehouse_id,
        defaults={"quantity": Decimal("0"), "locked_qty": Decimal("0"), "avg_cost": Decimal("0")},
    )
    # 重新查询并加行锁（get_or_create 不会加锁）
    inv = (
        Inventory.objects.select_for_update()
        .filter(product_id=product_id, warehouse_id=warehouse_id)
        .first()
    )
    return inv


def change_stock(
    product_id,
    warehouse_id,
    change_qty,
    biz_type,
    biz_id=None,
    biz_no="",
    remark="",
    avg_cost=None,
):
    """统一库存变更入口。

    :param change_qty: 正数表示增加（入库），负数表示减少（出库/退货）
    :raises ValueError: 可用库存不足时
    :returns: (Inventory, InventoryTransaction)
    """
    change_qty = Decimal(str(change_qty))
    if avg_cost is not None:
        avg_cost = Decimal(str(avg_cost))

    with transaction.atomic():
        inv = _get_or_create_locked(product_id, warehouse_id)

        # 出库类业务需校验可用库存
        if change_qty < 0:
            available = inv.quantity - inv.locked_qty
            if available + change_qty < 0:
                raise ValueError(
                    f"可用库存不足：现有可用 {available}，需要 {-change_qty}"
                )

        # 移动加权平均成本（仅入库正数且有成本时更新）
        if change_qty > 0 and avg_cost is not None:
            total_cost = inv.quantity * inv.avg_cost + change_qty * avg_cost
            new_qty = inv.quantity + change_qty
            inv.avg_cost = total_cost / new_qty if new_qty else Decimal("0")

        inv.quantity = F("quantity") + change_qty
        inv.save(update_fields=["quantity", "avg_cost", "updated_at"])
        inv.refresh_from_db()

        txn = InventoryTransaction.objects.create(
            product_id=product_id,
            warehouse_id=warehouse_id,
            biz_type=biz_type,
            biz_id=biz_id,
            biz_no=biz_no,
            change_qty=change_qty,
            after_qty=inv.quantity,
            remark=remark,
        )
        return inv, txn


# 便捷封装
def purchase_in(product_id, warehouse_id, qty, avg_cost=None, **kw):
    return change_stock(product_id, warehouse_id, qty, PURCHASE_IN, avg_cost=avg_cost, **kw)


def purchase_return(product_id, warehouse_id, qty, **kw):
    return change_stock(product_id, warehouse_id, -qty, PURCHASE_RETURN, **kw)


def sales_out(product_id, warehouse_id, qty, **kw):
    return change_stock(product_id, warehouse_id, -qty, SALES_OUT, **kw)


def sales_return(product_id, warehouse_id, qty, **kw):
    return change_stock(product_id, warehouse_id, qty, SALES_RETURN, **kw)


def stock_check_adjust(product_id, warehouse_id, diff_qty, **kw):
    return change_stock(product_id, warehouse_id, diff_qty, STOCK_CHECK, **kw)


def stock_transfer_move(product_id, warehouse_id, qty, **kw):
    return change_stock(product_id, warehouse_id, qty, STOCK_TRANSFER, **kw)
