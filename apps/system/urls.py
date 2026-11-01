"""system 应用路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    OperationLogViewSet,
    PermissionViewSet,
    RoleViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"roles", RoleViewSet, basename="roles")
router.register(r"permissions", PermissionViewSet, basename="permissions")
router.register(r"operation-logs", OperationLogViewSet, basename="operation-logs")

urlpatterns = [
    path("", include(router.urls)),
]
