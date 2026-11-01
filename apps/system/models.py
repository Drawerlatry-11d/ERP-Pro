"""系统/权限域模型：用户、部门、角色、权限、操作日志。

对应规划文档中的权限与系统域（sys_user / sys_role / sys_permission /
sys_user_role / sys_role_permission / sys_department / sys_operation_log）。
"""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra):
        if not username:
            raise ValueError("用户名不能为空")
        user = self.model(username=username, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra)

    def create_superuser(self, username, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_active", True)
        return self._create_user(username, password, **extra)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """系统用户（sys_user）。密码使用 Django 自带哈希，禁止明文。"""

    username = models.CharField("用户名", max_length=64, unique=True)
    real_name = models.CharField("姓名", max_length=64, blank=True, default="")
    email = models.EmailField("邮箱", blank=True, default="")
    phone = models.CharField("手机号", max_length=32, blank=True, default="")
    dept = models.ForeignKey(
        "system.Department",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="部门",
    )
    status = models.SmallIntegerField(
        "状态", default=1, choices=((1, "启用"), (0, "禁用"))
    )
    last_login_ip = models.CharField("最后登录IP", max_length=64, blank=True, default="")
    is_staff = models.BooleanField("可登录后台", default=False)
    is_active = models.BooleanField("激活", default=True)
    is_superuser = models.BooleanField("超级管理员", default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["real_name"]

    objects = UserManager()

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username


class Department(BaseModel):
    """部门/组织架构（sys_department）。"""

    name = models.CharField("部门名称", max_length=64)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="上级部门",
    )
    leader = models.CharField("负责人", max_length=64, blank=True, default="")
    sort = models.IntegerField("排序", default=0)

    class Meta:
        db_table = "sys_department"
        verbose_name = "部门"
        verbose_name_plural = "部门"

    def __str__(self):
        return self.name


class Role(BaseModel):
    """角色（sys_role）。"""

    name = models.CharField("角色名称", max_length=64)
    code = models.CharField("角色编码", max_length=64, unique=True)
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        db_table = "sys_role"
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.name


class Permission(BaseModel):
    """权限/菜单（sys_permission）。支持菜单、按钮、接口三类。"""

    TYPE_CHOICES = (
        ("menu", "菜单"),
        ("button", "按钮"),
        ("api", "接口"),
    )
    name = models.CharField("权限名称", max_length=64)
    code = models.CharField("权限编码", max_length=128, unique=True)
    type = models.CharField("类型", max_length=16, choices=TYPE_CHOICES, default="api")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="上级权限",
    )
    path = models.CharField("路由/接口路径", max_length=255, blank=True, default="")
    sort = models.IntegerField("排序", default=0)

    class Meta:
        db_table = "sys_permission"
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    """用户-角色关联（sys_user_role）。"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_roles", verbose_name="用户"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_users", verbose_name="角色"
    )

    class Meta:
        db_table = "sys_user_role"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"
        unique_together = (("user", "role"),)


class RolePermission(BaseModel):
    """角色-权限关联（sys_role_permission）。"""

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_perms", verbose_name="角色"
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="perm_roles",
        verbose_name="权限",
    )

    class Meta:
        db_table = "sys_role_permission"
        verbose_name = "角色权限"
        verbose_name_plural = "角色权限"
        unique_together = (("role", "permission"),)


class OperationLog(BaseModel):
    """操作审计日志（sys_operation_log）。关键动作全部留痕。"""

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="操作人"
    )
    action = models.CharField("操作", max_length=64)
    module = models.CharField("模块", max_length=64)
    ip = models.CharField("IP", max_length=64, blank=True, default="")
    detail = models.TextField("详情", blank=True, default="")

    class Meta:
        db_table = "sys_operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"
        ordering = ["-created_at"]
