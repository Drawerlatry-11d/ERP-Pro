"""reports 应用路由。"""
from django.urls import path

from .views import (
    DashboardView,
    ProfitAnalysisView,
    PurchaseSalesSummaryView,
)

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("purchase-sales/", PurchaseSalesSummaryView.as_view(), name="purchase-sales"),
    path("profit/", ProfitAnalysisView.as_view(), name="profit"),
]
