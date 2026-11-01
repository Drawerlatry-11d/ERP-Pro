"""purchase 应用 Admin 注册。"""
from django.contrib import admin

from .models import (
    PurchaseInbound,
    PurchaseInboundItem,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseReturn,
)

admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(PurchaseInbound)
admin.site.register(PurchaseInboundItem)
admin.site.register(PurchaseReturn)
