from django.urls import path
from .consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
]