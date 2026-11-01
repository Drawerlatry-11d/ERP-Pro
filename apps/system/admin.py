"""system 应用 Admin 注册。"""
from django.contrib import admin

from .models import (
    Department,
    OperationLog,
    Permission,
    Role,
    User,
    UserRole,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "real_name", "phone", "status", "is_staff"]
    search_fields = ["username", "real_name"]


admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(UserRole)
admin.site.register(OperationLog)
