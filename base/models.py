# Date 2018-03-12
# Author VanLiuZhi

from django.db import models
from base.fields import verbose_name as _
from django.utils import timezone
from django.utils.functional import cached_property
import datetime


class BaseModel(models.Model):
    ordering = models.IntegerField(_('排序权值'), default=0, db_index=True, editable=False)
    created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    date = models.DateField(_('创建日期'), default=timezone.now)  # titimezone 是系统设置时区
    updated = models.DateTimeField(_('修改时间'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-ordering', '-id']

    @cached_property
    def base_fields(self):
        """
        基本字段list（BaseModel的字段 + id）
        :return:
        """
        return [item.attname for item in BaseModel()._meta.concrete_fields]

    def get_fields(self, not_add_fields=True):
        """
        返回模型字典名称的list（不会返回id和基本字段，需要则手动添加）
        :param not_add_fields: 决定是否添加模型的add_fields属性里面的字段
        :return:
        """
        fields = [item.attname for item in self._meta.concrete_fields if item.attname not in self.base_fields]
        if getattr(self, 'add_fields', None) and not not_add_fields:
            add_fields = getattr(self, 'add_fields', [])
            fields += add_fields
        return fields

    def get_dict(self, not_add_fields=True, other_fields=[]):
        """
        返回模型实例的字典
        :return:
        """
        _dict = {}
        _field = self.get_fields(not_add_fields)
        _field += other_fields
        for item in _field:
            _dict[item] = getattr(self, item, '')
        return _dict
