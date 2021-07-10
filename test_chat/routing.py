import os
#
from django.core.asgi import get_asgi_application
#
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#
from chat.routing import url_patterns


#


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_chat.settings")

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            *url_patterns,
        ])
    ),
})