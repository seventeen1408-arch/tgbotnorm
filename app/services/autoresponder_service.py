"""
Сервис AutoResponder - автоматические ответы на сообщения.
"""

from app.core import get_logger

logger = get_logger(__name__)


class AutoResponderService:
    """Сервис автоматических ответов."""
    
    def __init__(self, db):
        self.db = db
    
    async def send_auto_response(self, user_id: int, message_type: str) -> str:
        """Отправить автоматический ответ."""
        responses = {
            "welcome": "👋 Добро пожаловать в наш бот!",
            "help": "📞 Для помощи свяжитесь с поддержкой.",
            "vip_offer": "💎 Хотите получить VIP доступ?",
            "signal_available": "📊 Новый сигнал доступен!",
        }
        
        response = responses.get(message_type, "Спасибо за ваше сообщение!")
        logger.info(f"📤 Отправлен автоответ пользователю {user_id}: {message_type}")
        return response
    
    async def log_interaction(self, user_id: int, message_type: str):
        """Логировать взаимодействие."""
        await self.db.create_event(user_id, "autoresponse", message_type)
