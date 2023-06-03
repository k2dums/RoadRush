"""
ASGI config for RoadRush project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RoadRush.settings")
django_asgi_app= get_asgi_application()

import rider.routing
import driver.routing
application=ProtocolTypeRouter(
    {
    'http':django_asgi_app,
    'websocket':#
    AuthMiddlewareStack(URLRouter(
    rider.routing.websocket_urlpatterns
    + driver.routing.websocket_urlpatterns))
    #)
    }
)
