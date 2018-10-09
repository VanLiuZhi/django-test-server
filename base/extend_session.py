#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 13:58
# @Author  : liuzhi
# @File    : extend_session.py

from django.contrib.sessions.backends.db import SessionStore as DBStore
# from django.contrib.sessions.base_session import AbstractBaseSession
# from django.db import models

import logging
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from django.contrib.sessions import middleware
from django.conf import settings


# class CustomSession(AbstractBaseSession):
#     account_id = models.IntegerField(null=True, db_index=True)
#
#     @classmethod
#     def get_session_store_class(cls):
#         return SessionStore
#
#
# class SessionStore(DBStore):
#     @classmethod
#     def get_model_class(cls):
#         return CustomSession
#
#     def create_model_instance(self, data):
#         obj = super().create_model_instance(data)
#         try:
#             account_id = int(data.get('_auth_user_id'))
#         except (ValueError, TypeError):
#             account_id = None
#         obj.account_id = account_id
#         return obj


class ExtendSessionStore(DBStore):
    def load(self):
        try:
            s = self.model.objects.get(
                session_key=self.session_key,
                expire_date__gt=timezone.now()
            )
            return self.decode(s.session_data)
        except (self.model.DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger('django.security.%s' % e.__class__.__name__)
                logger.warning(str(e))
            # self._session_key = None
            return {}


class ExtendSessionMiddleware(middleware.SessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None) or request.COOKIES.get('_token')
        request.session = ExtendSessionStore(session_key)
