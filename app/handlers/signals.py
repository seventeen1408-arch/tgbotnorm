"""
Обработчик сигналов.
"""

from aiogram import Router, F
from aiogram.types import Message
from app.core import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(F.text.contains("сигнал"))
async def handle_signals(message: Message, db, soft_gate_service):
    """Обработчик запроса сигналов."""
    user_id = message.from_user.id
    
    # Проверить доступ
    has_access = await soft_gate_service.check_access(user_id)
    
    if not has_access:
        await message.answer(
            "❌ У вас нет доступа к сигналам.\n"
            "💎 Приобретите VIP подписку или получите бесплатный доступ."
        )
        return
    
    # Получить сигналы
    signals = await db.get_signals()
    
    if not signals:
        await message.answer("📊 Сигналов нет.")
        return
    
    # Отправить сигналы
    signals_text = "📊 Доступные сигналы:\n\n"
    for signal in signals[:5]:  # Первые 5 сигналов
        signals_text += (
            f"🎯 {signal.game_name}\n"
            f"📈 Коэффициент: {signal.coefficient}\n"
            f"⏰ Время: {signal.time_utc} UTC\n\n"
        )
    
    await message.answer(signals_text)
    
    # Логировать событие
    await db.create_event(user_id, "signal_view")
