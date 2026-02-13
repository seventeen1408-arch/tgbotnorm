"""
Обработчик VIP предложений.
"""

from aiogram import Router, F
from aiogram.types import Message
from app.core import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(F.text.contains("vip"))
async def handle_vip_offer(message: Message, db):
    """Обработчик VIP предложений."""
    user_id = message.from_user.id
    
    logger.info(f"💎 VIP запрос от {user_id}")
    
    # Проверить есть ли уже VIP
    user = await db.get_user(user_id)
    if user and user.is_vip:
        await message.answer("✅ У вас уже есть VIP подписка!")
        return
    
    # Отправить VIP предложение
    vip_text = (
        "💎 VIP ПОДПИСКА\n\n"
        "Получите доступ к:\n"
        "✅ Всем сигналам\n"
        "✅ Эксклюзивному контенту\n"
        "✅ Приоритетной поддержке\n\n"
        "💰 Цена: 99 USDT/месяц\n\n"
        "Нажмите /buy_vip для покупки"
    )
    
    await message.answer(vip_text)
    
    # Логировать событие
    await db.create_event(user_id, "vip_offer_shown")
