"""finance 应用 Admin 注册。"""
from django.contrib import admin

from .models import (
    FinanceAccount,
    FinancePayable,
    FinancePayment,
    FinanceReceipt,
    FinanceReceivable,
)

admin.site.register(FinanceAccount)
admin.site.register(FinanceReceivable)
admin.site.register(FinancePayable)
admin.site.register(FinanceReceipt)
admin.site.register(FinancePayment)
