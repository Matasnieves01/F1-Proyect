from domain.entities.chat_messages import ChatMessage
from infrastructure.repositories.chat_repository import save_chat_message
from datetime import datetime

def handle_maessage(user, content):
    message = ChatMessage(user=user, content=content, timestamp=datetime.now())
    save_chat_message(message)
    return message