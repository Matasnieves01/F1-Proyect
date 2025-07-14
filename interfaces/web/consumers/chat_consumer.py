from channels.generic.websocket import AsyncWebsocketConsumer
import json
from use_cases.chat_service import handle_maessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'live_chat'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def desconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"].username if self.scope["user"].is_authenticated else "Anónimo"
        content = data["message"]

        message = handle_maessage(user, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message.content,
                "user": message.user,
                "timestamp": message.timestamp.strftime("%H:%M")
            }
        )

        async def chat_message(self, event):
            await self.send(text_data=json.dumps({
                "user": event["user"],
                "message": event["message"],
                "timestamp": event["timestamp"]
            })) 