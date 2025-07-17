import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from infrastructure.repositories.chat_repository import save_chat_message
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_group'
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'
        chat_entity = type('ChatEntity', (), {'user': user, 'content': message, 'timestamp': None})()
        await save_chat_message(chat_entity)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'timestamp': datetime.now().strftime('%H:%M:%S')  # Agregar timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event.get('timestamp', 'N/A')  # Obtener timestamp o usar valor por defecto
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'timestamp': timestamp
        }))