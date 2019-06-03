# -*- coding:utf-8 -*-
# Author:DaoYang

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from colorfight import views

urlpatterns = [
    # 首页

    re_path('colorfight/index/', views.index),
    re_path('colorfight/createtest/', views.createtest),
    re_path('colorfight/download/', views.download),
    re_path('colorfight/instructions/', views.instructions),
    re_path('colorfight/getgameinfo/', views.getgameinfo),
    re_path('colorfight/matchmsg/', views.matchmsg),
    re_path('colorfight/document/', views.document),
    re_path('colorfight/contactme/', views.contactme),
    re_path(r'^colorfight/AI_test/(?P<game_id>[0-9]{5})/', views.colorfight_test, name='game_id'),
]