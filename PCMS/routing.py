# -*- coding:utf-8 -*-
# Author:DaoYang

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import snake.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            snake.routing.websocket_urlpatterns
        )
    ),
})