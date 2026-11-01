"""system 应用序列化器。"""
from rest_framework import serializers

from .models import (
    Department,
    OperationLog,
    Permission,
    Role,
    User,
    UserRole,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    dept_name = serializers.CharField(source="dept.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "real_name",
            "email",
            "phone",
            "dept",
            "dept_name",
            "status",
            "last_login_ip",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password("123456")  # 默认初始密码
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "parent", "leader", "sort"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "code", "remark"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "code", "type", "parent", "path", "sort"]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["id", "user", "role"]


class OperationLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = OperationLog
        fields = ["id", "user", "user_name", "action", "module", "ip", "detail", "created_at"]
