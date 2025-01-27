from django.urls import re_path
from .consumers import ChatConsumer

# Define WebSocket URL routing
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
