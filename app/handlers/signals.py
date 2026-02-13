"""
Обработчик сигналов для игр.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.core import get_logger
from app.database.db import db
from app.services.soft_gate_service import SoftGateService

logger = get_logger(__name__)
router = Router()


@router.message(Command("signals"))
async def cmd_signals(message: Message):
    """Обработчик команды /signals."""
    user_id = message.from_user.id
    
    logger.info(f"📊 Запрос сигналов от пользователя {user_id}")
    
    try:
        # Проверить доступ
        soft_gate = SoftGateService(db)
        has_access = await soft_gate.check_access(user_id)
        
        if not has_access:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💎 Получить VIP", callback_data="vip_subscribe")],
                    [InlineKeyboardButton(text="🎁 Бесплатный доступ", callback_data="free_access")],
                ]
            )
            await message.answer(
                "❌ У вас нет доступа к сигналам.\n\n"
                "💎 Приобретите VIP подписку или получите бесплатный доступ.",
                reply_markup=keyboard
            )
            return
        
        # Получить сигналы из БД
        signals = await db.get_signals()
        
        if not signals:
            await message.answer(
                "📊 Сигналов нет.\n\n"
                "Сигналы обновляются каждый час. Проверьте позже!"
            )
            return
        
        # Отправить сигналы
        signals_text = "📊 **ДОСТУПНЫЕ СИГНАЛЫ**\n\n"
        for i, signal in enumerate(signals[:10], 1):  # Первые 10 сигналов
            signals_text += (
                f"{i}. 🎯 {signal.get('game_name', 'Unknown')}\n"
                f"   📈 Коэффициент: {signal.get('coefficient', 'N/A')}\n"
                f"   ⏰ Время: {signal.get('time_utc', 'N/A')} UTC\n"
                f"   💰 Рекомендуемая ставка: {signal.get('recommended_bet', 'N/A')}\n\n"
            )
        
        await message.answer(signals_text)
        
        # Логировать событие
        await db.create_event(user_id, "signal_view", f"Просмотрено {len(signals)} сигналов")
        logger.info(f"✅ Сигналы отправлены пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_signals: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении сигналов. Попробуйте позже.")


@router.message(F.text.contains("сигнал"))
async def handle_signals_text(message: Message):
    """Обработчик текстовых запросов о сигналах."""
    user_id = message.from_user.id
    
    logger.info(f"📊 Текстовый запрос сигналов от пользователя {user_id}")
    
    try:
        # Проверить доступ
        soft_gate = SoftGateService(db)
        has_access = await soft_gate.check_access(user_id)
        
        if not has_access:
            await message.answer(
                "❌ У вас нет доступа к сигналам.\n"
                "💎 Приобретите VIP подписку для получения сигналов.\n\n"
                "Используйте команду /vip для подробной информации."
            )
            return
        
        # Получить последний сигнал
        signals = await db.get_signals()
        
        if not signals:
            await message.answer("📊 Сигналов нет. Проверьте позже!")
            return
        
        signal = signals[0]  # Последний сигнал
        
        signal_text = (
            f"🎯 **Последний сигнал**\n\n"
            f"Игра: {signal.get('game_name', 'Unknown')}\n"
            f"Коэффициент: {signal.get('coefficient', 'N/A')}\n"
            f"Время: {signal.get('time_utc', 'N/A')} UTC\n"
            f"Рекомендуемая ставка: {signal.get('recommended_bet', 'N/A')}\n\n"
            f"Используйте /signals для просмотра всех сигналов."
        )
        
        await message.answer(signal_text)
        
        # Логировать событие
        await db.create_event(user_id, "signal_request", signal.get('game_name', 'Unknown'))
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_signals_text: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении сигнала.")
