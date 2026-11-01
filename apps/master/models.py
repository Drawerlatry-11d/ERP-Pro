"""主数据域模型：商品/分类、计量单位、仓库、客户、供应商。

对应规划文档主数据域（base_product / base_category / base_unit /
base_warehouse / base_customer / base_supplier）。
"""
from django.db import models

from apps.common.models import BaseModel


class Category(BaseModel):
    """商品分类（base_category），支持树形结构。"""

    name = models.CharField("分类名称", max_length=64)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="上级分类",
    )
    sort = models.IntegerField("排序", default=0)
    status = models.SmallIntegerField(
        "状态", default=1, choices=((1, "启用"), (0, "停用"))
    )

    class Meta:
        db_table = "base_category"
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"

    def __str__(self):
        return self.name


class Unit(BaseModel):
    """计量单位（base_unit）。"""

    name = models.CharField("名称", max_length=32)
    symbol = models.CharField("符号", max_length=16, blank=True, default="")

    class Meta:
        db_table = "base_unit"
        verbose_name = "计量单位"
        verbose_name_plural = "计量单位"

    def __str__(self):
        return self.name


class Product(BaseModel):
    """商品（base_product）。"""

    sku = models.CharField("SKU编码", max_length=64, unique=True)
    name = models.CharField("商品名称", max_length=128)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="分类",
    )
    unit = models.ForeignKey(
        Unit,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="计量单位",
    )
    spec = models.CharField("规格", max_length=128, blank=True, default="")
    barcode = models.CharField("条码", max_length=64, blank=True, default="")
    sale_price = models.DecimalField("售价", max_digits=18, decimal_places=2, default=0)
    cost_price = models.DecimalField("成本价", max_digits=18, decimal_places=2, default=0)
    status = models.SmallIntegerField(
        "状态", default=1, choices=((1, "在售"), (0, "下架"))
    )

    class Meta:
        db_table = "base_product"
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return f"{self.name}({self.sku})"


class Warehouse(BaseModel):
    """仓库（base_warehouse）。"""

    name = models.CharField("仓库名称", max_length=64)
    location = models.CharField("位置", max_length=128, blank=True, default="")
    keeper = models.CharField("保管员", max_length=64, blank=True, default="")

    class Meta:
        db_table = "base_warehouse"
        verbose_name = "仓库"
        verbose_name_plural = "仓库"

    def __str__(self):
        return self.name


class Customer(BaseModel):
    """客户（base_customer），含信用额度与欠款。"""

    name = models.CharField("客户名称", max_length=128)
    contact = models.CharField("联系人", max_length=64, blank=True, default="")
    phone = models.CharField("电话", max_length=32, blank=True, default="")
    level = models.CharField("等级", max_length=32, blank=True, default="")
    credit_limit = models.DecimalField(
        "信用额度", max_digits=18, decimal_places=2, default=0
    )
    arrears = models.DecimalField("欠款", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "base_customer"
        verbose_name = "客户"
        verbose_name_plural = "客户"

    def __str__(self):
        return self.name


class Supplier(BaseModel):
    """供应商（base_supplier）。"""

    name = models.CharField("供应商名称", max_length=128)
    contact = models.CharField("联系人", max_length=64, blank=True, default="")
    phone = models.CharField("电话", max_length=32, blank=True, default="")
    level = models.CharField("等级", max_length=32, blank=True, default="")
    payment_terms = models.CharField("账期", max_length=64, blank=True, default="")

    class Meta:
        db_table = "base_supplier"
        verbose_name = "供应商"
        verbose_name_plural = "供应商"

    def __str__(self):
        return self.name
