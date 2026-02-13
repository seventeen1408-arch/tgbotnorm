"""
Сервис управления подписками VIP.
"""

from datetime import datetime, timedelta
from typing import Optional
from aiogram import Bot
from app.core.logger import get_logger
from app.database.db import db

logger = get_logger(__name__)


class SubscriptionService:
    """Управление VIP подписками."""
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def is_vip(self, user_id: int) -> bool:
        """Проверить VIP статус."""
        try:
            user = await db.get_user(user_id)
            return user and user.get("is_vip", False)
        except Exception as e:
            logger.error(f"Ошибка проверки VIP: {e}")
            return False
    
    async def activate_vip(self, user_id: int, days: int = 30) -> bool:
        """Активировать VIP."""
        try:
            expires_at = datetime.utcnow() + timedelta(days=days)
            await db.update_user(user_id, {
                "is_vip": True,
                "vip_expires_at": expires_at
            })
            logger.info(f"VIP активирован для {user_id} на {days} дней")
            return True
        except Exception as e:
            logger.error(f"Ошибка активации VIP: {e}")
            return False
    
    async def deactivate_vip(self, user_id: int) -> bool:
        """Деактивировать VIP."""
        try:
            await db.update_user(user_id, {"is_vip": False})
            logger.info(f"VIP деактивирован для {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка деактивации VIP: {e}")
            return False
