"""RBAC 权限校验辅助（预留，后续按 permission.code 做接口级鉴权）。"""
from rest_framework.permissions import BasePermission


class HasPerm(BasePermission):
    """校验当前用户是否拥有指定权限编码。

    用法：
        permission_classes = [HasPerm.with_code("purchase:order:create")]
    """

    code = None

    def __init__(self, code=None):
        self.code = code or self.code

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        # 超管放行；普通用户后续根据 RolePermission 关联校验
        # TODO: 接入缓存后的角色-权限集合做二次校验
        return True

    @classmethod
    def with_code(cls, code):
        return type("HasPerm", (HasPerm,), {"code": code})
