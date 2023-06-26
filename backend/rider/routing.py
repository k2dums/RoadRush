from django.urls import re_path
from . import consumers

websocket_urlpatterns=[
    re_path(r"ws/rider/(?P<rider_name>\w+)/$",consumers.RiderConsumer.as_asgi())
]