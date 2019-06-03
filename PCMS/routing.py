# -*- coding:utf-8 -*-
# Author:DaoYang

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import channel_routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            channel_routing.websocket_urlpatterns,
        )
    ),
})
