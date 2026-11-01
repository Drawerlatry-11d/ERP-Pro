"""master 应用 Admin 注册。"""
from django.contrib import admin

from .models import Category, Customer, Product, Supplier, Unit, Warehouse

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Customer)
admin.site.register(Supplier)
