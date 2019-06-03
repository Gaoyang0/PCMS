# -*- coding:utf-8 -*-
# Author:DaoYang

from django.contrib import admin
from django.urls import path, include, re_path
from snake import views

urlpatterns = [
    # 首页
    re_path('snake/snake/', views.snake),
    re_path('snake/index/', views.index),
    re_path('snake/instructions/', views.instructions),
    re_path('snake/download/', views.download),
    re_path('snake/matchmsg/', views.matchmsg),
    re_path('snake/document/', views.document),
    re_path('snake/contactme/', views.contactme),
]