"""财务域模型（P1）：应收、应付、收付款、资金账户。

对应规划文档财务域（finance_receivable / finance_payable /
finance_receipt / finance_payment / finance_account）。二期实现。
"""
from django.db import models

from apps.common.constants import DOCUMENT_STATUS
from apps.common.models import BaseModel
from apps.master.models import Customer, Supplier
from apps.system.models import User


class FinanceAccount(BaseModel):
    """资金账户（finance_account）：银行/现金/支付宝等。"""

    name = models.CharField("账户名称", max_length=64)
    type = models.CharField(
        "类型", max_length=16, choices=(("bank", "银行"), ("cash", "现金"), ("online", "线上")), default="bank"
    )
    balance = models.DecimalField("余额", max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "finance_account"
        verbose_name = "资金账户"
        verbose_name_plural = "资金账户"

    def __str__(self):
        return self.name


class FinanceReceivable(BaseModel):
    """应收（finance_receivable），关联销售单/客户。"""

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="receivables", verbose_name="客户"
    )
    amount = models.DecimalField("应收金额", max_digits=18, decimal_places=2, default=0)
    remained = models.DecimalField("未收金额", max_digits=18, decimal_places=2, default=0)
    due_date = models.DateField("到期日", null=True, blank=True)
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="PENDING")

    class Meta:
        db_table = "finance_receivable"
        verbose_name = "应收"
        verbose_name_plural = "应收"


class FinancePayable(BaseModel):
    """应付（finance_payable），关联采购单/供应商。"""

    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="payables", verbose_name="供应商"
    )
    amount = models.DecimalField("应付金额", max_digits=18, decimal_places=2, default=0)
    remained = models.DecimalField("未付金额", max_digits=18, decimal_places=2, default=0)
    due_date = models.DateField("到期日", null=True, blank=True)
    status = models.CharField("状态", max_length=16, choices=DOCUMENT_STATUS, default="PENDING")

    class Meta:
        db_table = "finance_payable"
        verbose_name = "应付"
        verbose_name_plural = "应付"


class FinanceReceipt(BaseModel):
    """收款单（finance_receipt），客户回款。"""

    receipt_no = models.CharField("收款单号", max_length=64, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="receipts", verbose_name="客户"
    )
    account = models.ForeignKey(
        FinanceAccount, on_delete=models.PROTECT, related_name="receipts", verbose_name="账户"
    )
    amount = models.DecimalField("收款金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )

    class Meta:
        db_table = "finance_receipt"
        verbose_name = "收款单"
        verbose_name_plural = "收款单"


class FinancePayment(BaseModel):
    """付款单（finance_payment），供应商付款。"""

    payment_no = models.CharField("付款单号", max_length=64, unique=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="payments", verbose_name="供应商"
    )
    account = models.ForeignKey(
        FinanceAccount, on_delete=models.PROTECT, related_name="payments", verbose_name="账户"
    )
    amount = models.DecimalField("付款金额", max_digits=18, decimal_places=2, default=0)
    handler = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="经办人"
    )

    class Meta:
        db_table = "finance_payment"
        verbose_name = "付款单"
        verbose_name_plural = "付款单"
