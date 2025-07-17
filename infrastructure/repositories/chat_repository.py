from core.models import ChatMessage as ChatModel

def save_chat_message(chat_entity):
    return ChatModel.objects.create(
        user=chat_entity.user,
        content=chat_entity.content,
        timestamp=chat_entity.timestamp
    )
