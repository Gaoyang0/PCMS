# -*- coding:utf-8 -*-
# Author:DaoYang

from django.conf.urls import url

from snake import consumers as snake_consumers
from colorfight import consumers as colorfight_consumers


websocket_urlpatterns = [
    # snake
    url(r'^ws/test/(?P<room_name>[^/]+)/', snake_consumers.SnakeConsumer),
    # colorfight
    url(r'^ws/colorfight/action_channel/(?P<game_id>[0-9]{5})/(?P<user_name>[^/]+)/', colorfight_consumers.ActionConsumer),
    url(r'^ws/colorfight/game_channel/(?P<game_id>[0-9]{5})/(?P<user_name>[^/]+)/', colorfight_consumers.GameConsumer),
]