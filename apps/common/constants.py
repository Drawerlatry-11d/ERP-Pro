"""库存业务类型常量（inventory_transaction.biz_type）。"""

# 单据状态通用：草稿 / 待审核 / 已审核 / 已作废
DRAFT = "DRAFT"
PENDING = "PENDING"
APPROVED = "APPROVED"
CANCELLED = "CANCELLED"

DOCUMENT_STATUS = [
    (DRAFT, "草稿"),
    (PENDING, "待审核"),
    (APPROVED, "已审核"),
    (CANCELLED, "已作废"),
]

# 库存流水业务类型
PURCHASE_IN = "PURCHASE_IN"          # 采购入库
PURCHASE_RETURN = "PURCHASE_RETURN"  # 采购退货
SALES_OUT = "SALES_OUT"              # 销售出库
SALES_RETURN = "SALES_RETURN"        # 销售退货
STOCK_CHECK = "STOCK_CHECK"          # 盘点调整
STOCK_TRANSFER = "STOCK_TRANSFER"    # 调拨

INVENTORY_BIZ_TYPES = [
    (PURCHASE_IN, "采购入库"),
    (PURCHASE_RETURN, "采购退货"),
    (SALES_OUT, "销售出库"),
    (SALES_RETURN, "销售退货"),
    (STOCK_CHECK, "盘点调整"),
    (STOCK_TRANSFER, "调拨"),
]
