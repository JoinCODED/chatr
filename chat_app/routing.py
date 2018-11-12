from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import my_messages.routing


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)\
    'websocket': AuthMiddlewareStack(
        URLRouter(
            my_messages.routing.websocket_urlpatterns
        )
    ),
})
