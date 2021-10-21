"""
ASGI config for wheel_of_jeopardy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# Python Standard Libaries
import os

# Django Apps Modules
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# User Created Apps
import websockets.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wheel_of_jeopardy.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websockets.routing.websocket_urlpatterns
        )
    )
})