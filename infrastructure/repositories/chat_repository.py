import asyncio
from asgiref.sync import sync_to_async
from core.models import ChatMessage as ChatModel

# Función síncrona original
def save_chat_message_sync(chat_entity):
    return ChatModel.objects.create(
        user=chat_entity.user,
        content=chat_entity.content,
        timestamp=chat_entity.timestamp
    )

# Función asíncrona que envuelve la síncrona
save_chat_message = sync_to_async(save_chat_message_sync)