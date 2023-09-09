from django.urls import re_path
from . import consumers
websocket_urlpatterns=[
    re_path(r"ws/driver/(?P<driver_username>\w+)/$",consumers.DriverConsumer.as_asgi())
]