"""
Сервис PostbackPro - отслеживание постбеков от казино.
"""

import json
import hmac
import hashlib
from app.core import get_logger, config

logger = get_logger(__name__)


class PostbackProService:
    """Сервис обработки постбеков."""
    
    def __init__(self, db):
        self.db = db
    
    def verify_signature(self, data: str, signature: str) -> bool:
        """Проверить подпись постбека."""
        if not config.POSTBACK_SECRET:
            logger.warning("⚠️ POSTBACK_SECRET не установлен")
            return False
        
        expected_signature = hmac.new(
            config.POSTBACK_SECRET.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    async def process_postback(self, user_id: int, casino_id: str, 
                               event_type: str, amount: float, raw_data: str) -> bool:
        """Обработать постбек от казино."""
        try:
            # Создать запись постбека
            postback = await self.db.create_postback(
                user_id=user_id,
                casino_id=casino_id,
                event_type=event_type,
                amount=amount,
                raw_data=raw_data
            )
            
            logger.info(
                f"✅ Постбек обработан: пользователь {user_id}, "
                f"казино {casino_id}, событие {event_type}, сумма {amount}"
            )
            
            # Обновить информацию пользователя если это депозит
            if event_type == "deposit":
                user = await self.db.get_user(user_id)
                if user:
                    new_deposit = (user.deposit_amount or 0) + amount
                    await self.db.update_user(user_id, deposit_amount=new_deposit)
                    logger.info(f"💰 Обновлен депозит пользователя {user_id}: {new_deposit}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка обработки постбека: {e}")
            return False
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Получить статистику пользователя."""
        user = await self.db.get_user(user_id)
        if not user:
            return {}
        
        return {
            "user_id": user.user_id,
            "is_vip": user.is_vip,
            "deposit_amount": user.deposit_amount,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
