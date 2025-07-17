from domain.entities.chat_messages import ChatMessage
from infrastructure.repositories.chat_repository import save_chat_message
from datetime import datetime

def handle_message(user, content):
    message = ChatMessage(user=user, content=content, timestamp=datetime.now())
    save_chat_message(message)
    return message

    if not content or not user:
        raise ValueError("Content and user are required")
    
    message = ChatMessage(
        user=user[:255],
        content=content,
        timestamp=datetime.now()
    )
    return save_chat_message(message)
