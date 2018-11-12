from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import my_messages.routing
from my_messages.token_auth import TokenAuthMiddleware


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)\
    'websocket': TokenAuthMiddleware(
        URLRouter(
            my_messages.routing.websocket_urlpatterns
        )
    ),
})
