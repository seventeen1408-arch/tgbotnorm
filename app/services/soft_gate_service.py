"""
Сервис SoftGate - управление доступом к контенту.
"""

from datetime import datetime, timedelta
from app.core import get_logger

logger = get_logger(__name__)


class SoftGateService:
    """Сервис управления доступом к контенту."""
    
    def __init__(self, db):
        self.db = db
    
    async def check_access(self, user_id: int) -> bool:
        """Проверить доступ пользователя."""
        user = await self.db.get_user(user_id)
        if not user:
            return False
        
        # Если VIP - полный доступ
        if user.is_vip:
            return True
        
        # Если есть бесплатный доступ до определенного времени
        if user.signals_unlocked_until and user.signals_unlocked_until > datetime.utcnow():
            return True
        
        return False
    
    async def grant_free_access(self, user_id: int, duration_minutes: int = 120):
        """Дать бесплатный доступ на определенное время."""
        expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
        await self.db.update_user(user_id, signals_unlocked_until=expires_at)
        logger.info(f"✅ Бесплатный доступ выдан пользователю {user_id} на {duration_minutes} минут")
    
    async def grant_vip(self, user_id: int, duration_hours: int = 24):
        """Дать VIP статус."""
        expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        await self.db.update_user(user_id, is_vip=True, signals_unlocked_until=expires_at)
        logger.info(f"✅ VIP статус выдан пользователю {user_id} на {duration_hours} часов")
    
    async def revoke_access(self, user_id: int):
        """Отозвать доступ."""
        await self.db.update_user(user_id, signals_unlocked_until=None)
        logger.info(f"✅ Доступ отозван для пользователя {user_id}")
    
    async def check_and_unlock_signals(self):
        """Проверить и разблокировать сигналы для пользователей."""
        logger.info("🔍 Проверка и разблокировка сигналов...")
        # Логика проверки и разблокировки
        pass
