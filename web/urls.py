# -*- coding:utf-8 -*-
# Author:DaoYang

from django.contrib import admin
from django.urls import path, include, re_path
from web import views

urlpatterns = [
    # 首页
    re_path('web/index/', views.index),
    re_path('web/test/', views.test),
]