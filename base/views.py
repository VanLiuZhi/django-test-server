# Date 2018-03-20
# Author VanLiu

# from django.shortcuts import render
from django.template import loader
from django.views.generic.base import View
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.conf import settings
# from mongodbmanage.base import mongo_connection
import json
from django.shortcuts import render, HttpResponse
from base.util import json_filed_default


class SessionMinx:
    """
    session处理类
    """

    def get_session(self):
        return self.request.session

    def session_get(self, k):
        return self.get_session()[k] if k in self.get_session() else None

    def session_del(self, k):
        if k in self.get_session():
            del self.get_session()[k]

    def session_set(self, k, v):
        self.get_session()[k] = v

    def session_get_once(self, k):
        """
        该方法获取一次数据就从session中删除
        :param k:
        :return:
        """
        v = self.session_get(k)
        self.session_del(k)
        return v


class ResponseMinx:
    """
    响应处理类 #TODO 验证每次连接是不是都会创建新的对象，让响应方法得到新的参数（或者考虑单实例）
    """
    code = '0'
    data = ''
    msg = '请求成功'
    SUCCESS_CODE = '0'
    ERROR_CODE = '-1'

    test_param = '123'

    @property
    def return_result_data(self):
        result_data = {
            'code': self.code,
            'data': self.data,
            'msg': self.msg
        }
        print(self.test_param)
        self.test_param = '321'
        return result_data

    def success_response(self, data=None, msg=None, code=None):
        self.code = code or self.SUCCESS_CODE
        if data:
            self.data = data
        if msg:
            self.msg = msg
        return self.return_result_data

    def error_response(self, data=None, msg=None, code=None):
        self.code = code or self.ERROR_CODE
        if data:
            self.data = data
        if msg:
            self.msg = msg
        return self.return_result_data


class BaseView(View, ResponseMinx):
    template_name = None

    def render(self, template_name, context=None, request=None, content_type=None, status=None, using=None):
        """
        render extend, request is optional
        """
        if context is None or not isinstance(context, dict):
            context = {}
        context['view'] = self.__class__.__name__
        context['view_path'] = getattr(self, 'file_path', '')
        context['STATIC_URL'] = settings.STATIC_URL
        context['IS_DEBUG'] = settings.DEBUG
        content = loader.render_to_string(template_name, context, request=request, using=using)
        return HttpResponse(content, content_type, status)

    def xml_response_for_json(self, data):
        return HttpResponse(json.dumps(data, default=json_filed_default))
