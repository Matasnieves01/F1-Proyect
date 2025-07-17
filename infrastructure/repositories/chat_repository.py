import asyncio
from asgiref.sync import sync_to_async
from core.models import ChatMessage as ChatModel


def save_chat_message_sync(chat_entity):
    return ChatModel.objects.create(
        user=chat_entity.user,
        content=chat_entity.content
    )

# Asynchronous wrapper for use in async consumers
# Función asíncrona que envuelve la síncrona
save_chat_message = sync_to_async(save_chat_message_sync)