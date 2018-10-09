#!/usr/bin/env python
# Date 2018-03-20
# Author VanLiu

from django.shortcuts import render, HttpResponse
from base.views import BaseView
from django.urls import path
import json
from django.views.decorators.csrf import csrf_exempt


class IndexView(BaseView):
    # @csrf_exempt
    def post(self, request):
        return HttpResponse(json.dumps({'a': 123}))

    def get(self, request):
        print(request)
        return self.render("index.html")


class VadminView(BaseView):
    # @csrf_exempt
    def post(self, request):
        return HttpResponse(json.dumps({'a': 123}))

    def get(self, request):
        print(request)
        return self.render("vadmin_index.html")


urlpatterns = [
    path('vadmin', csrf_exempt(VadminView.as_view())),
    path('work', csrf_exempt(IndexView.as_view())),
]
