"""sales 应用 Admin 注册。"""
from django.contrib import admin

from .models import (
    SalesOrder,
    SalesOrderItem,
    SalesOutbound,
    SalesOutboundItem,
    SalesReturn,
)

admin.site.register(SalesOrder)
admin.site.register(SalesOrderItem)
admin.site.register(SalesOutbound)
admin.site.register(SalesOutboundItem)
admin.site.register(SalesReturn)
