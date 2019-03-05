# -*- coding:utf-8 -*-
# Author:DaoYang

from django.conf.urls import url

from . import consumers


websocket_urlpatterns = [
    url(r'^ws/test/(?P<room_name>[^/]+)/$', consumers.SnakeConsumer),
]