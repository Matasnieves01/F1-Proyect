from django.urls import re_path
from interfaces.web.consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/live-chat/$", ChatConsumer.as_asgi()),
]