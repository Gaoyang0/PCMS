# -*- coding:utf-8 -*-
# Author:DaoYang

from django.contrib import admin
from django.urls import path, include, re_path
from snake import views

urlpatterns = [
    # 首页
    re_path('snake/$', views.snake),
    re_path('control/$', views.control),
]