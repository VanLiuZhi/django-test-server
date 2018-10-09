#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 19:11
# @Author  : liuzhi
# @File    : util.py


def get_uuid():
    """
    利用uuid5 生成唯一id(基于MAC地址)
    :return:
    """
    import uuid
    # res = uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org') # (基于命名空间和一个字符的SHA-1加密的UUID)
    res = uuid.uuid1()
    return res


def request_body_to_dict(request):
    """
    转换XMLHttpRequest请求的数据(前端请求使用axios默认配置)
    :param request:
    :return:
    """
    import json
    _str = bytes.decode(request.body)
    data = _str and json.loads(_str) or _str
    return data


def dict_to_object(data, object):
    """
    把字典的数据赋值到某个对象的属性上
    :param data:
    :param object:
    :return:
    """
    for key, value in data.items():
        if hasattr(object, key):
            setattr(object, key, value)
    return object


def object_to_dict(fields, object):
    """
    把对象序列化成字典
    :param fields:
    :param object:
    :return:
    """
    _dict = {}
    for item in fields:
        _dict[item] = getattr(object, item)
    return _dict


def json_filed_default(obj):
    """
    处理不能被直接序列化的对象
    :param obj:
    :return:
    """
    import decimal
    import datetime
    import time
    from django.db.models.fields.files import ImageFieldFile
    from django.db.models.query import QuerySet
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %X')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    if isinstance(obj, datetime.time):
        return obj.strftime('%H:%M:%S')
    if isinstance(obj, time.struct_time):
        return {"timestamp": time.mktime(obj), "date": time.strftime('%Y-%m-%d', obj)}
    if isinstance(obj, ImageFieldFile):
        if hasattr(obj, 'url'):
            return obj.url
        else:
            return ''
    if isinstance(obj, QuerySet):
        return [o for o in obj]
    if hasattr(obj, 'to_json'):
        to_json = obj.to_json
        return to_json() if callable(to_json) else to_json
    raise TypeError(type(obj))
