"""公共基础模型：软删除 + 时间戳 + 统一主键。"""
from django.db import models


class ActiveManager(models.Manager):
    """仅返回未删除记录的默认管理器。"""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """所有业务表的公共基类。

    - id：BIGINT 自增主键
    - created_at / updated_at：时间戳
    - is_deleted：软删除标记（0/1）
    """

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    is_deleted = models.BooleanField("是否删除", default=False, db_index=True)

    objects = ActiveManager()
    all_objects = models.Manager()  # 包含已删除

    class Meta:
        abstract = True
