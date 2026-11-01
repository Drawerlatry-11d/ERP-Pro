"""ERP-Pro 主路由。"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 业务模块 API
    path("api/system/", include("apps.system.urls")),
    path("api/master/", include("apps.master.urls")),
    path("api/purchase/", include("apps.purchase.urls")),
    path("api/sales/", include("apps.sales.urls")),
    path("api/inventory/", include("apps.inventory.urls")),
    path("api/finance/", include("apps.finance.urls")),
    path("api/reports/", include("apps.reports.urls")),
    # API 文档（Swagger / OpenAPI）
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
