"""inventory 应用 Admin 注册。"""
from django.contrib import admin

from .models import (
    Inventory,
    InventoryTransaction,
    StockCheck,
    StockCheckItem,
    StockTransfer,
)

admin.site.register(Inventory)
admin.site.register(InventoryTransaction)
admin.site.register(StockCheck)
admin.site.register(StockCheckItem)
admin.site.register(StockTransfer)
