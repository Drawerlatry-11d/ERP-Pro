"""system 应用视图：RBAC 基础 CRUD。"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Department, OperationLog, Permission, Role, User
from .serializers import (
    DepartmentSerializer,
    OperationLogSerializer,
    PermissionSerializer,
    RoleSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["status", "dept"]
    search_fields = ["username", "real_name", "phone"]

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ["parent"]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ["name", "code"]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ["type", "parent"]


class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    filterset_fields = ["module", "action", "user"]
