"""
Обработчик текстовых сообщений.
"""

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.core import get_logger
from app.database.db import db
from app.services.autoresponder_service import AutoResponderService

logger = get_logger(__name__)
router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    """Обработчик всех текстовых сообщений."""
    user_id = message.from_user.id
    text = message.text
    
    logger.info(f"💬 Сообщение от {user_id}: {text}")
    
    try:
        # Логировать событие
        await db.create_event(user_id, "message_received", text)
        
        # Проверить ключевые слова
        text_lower = text.lower()
        
        if "помощь" in text_lower or "help" in text_lower:
            help_text = (
                "❓ **СПРАВКА**\n\n"
                "Доступные команды:\n"
                "/start - Начало\n"
                "/signals - Сигналы\n"
                "/vip - VIP подписка\n"
                "/profile - Профиль\n"
                "/balance - Баланс\n"
                "/help - Справка\n\n"
                "Используйте команды выше!"
            )
            await message.answer(help_text)
        
        elif "сигнал" in text_lower or "signal" in text_lower:
            signal_text = (
                "📊 **СИГНАЛЫ**\n\n"
                "Используйте команду /signals для просмотра всех сигналов.\n\n"
                "Или нажмите кнопку ниже:"
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📊 Просмотреть сигналы", callback_data="signals")],
                ]
            )
            await message.answer(signal_text, reply_markup=keyboard)
        
        elif "vip" in text_lower or "вип" in text_lower:
            vip_text = (
                "💎 **VIP ПОДПИСКА**\n\n"
                "Получите доступ к эксклюзивным функциям!\n\n"
                "Используйте команду /vip для подробной информации."
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💎 Получить VIP", callback_data="vip_1month")],
                ]
            )
            await message.answer(vip_text, reply_markup=keyboard)
        
        elif "профиль" in text_lower or "profile" in text_lower:
            profile_text = (
                "👤 **МОЙ ПРОФИЛЬ**\n\n"
                "Используйте команду /profile для просмотра профиля."
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
                ]
            )
            await message.answer(profile_text, reply_markup=keyboard)
        
        elif "баланс" in text_lower or "balance" in text_lower:
            balance_text = (
                "💰 **МОЙ БАЛАНС**\n\n"
                "Используйте команду /balance для просмотра баланса."
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
                ]
            )
            await message.answer(balance_text, reply_markup=keyboard)
        
        elif "поддержка" in text_lower or "support" in text_lower:
            support_text = (
                "📞 **ПОДДЕРЖКА**\n\n"
                "Нажмите кнопку ниже для связи с поддержкой."
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📞 Связаться с поддержкой", url="https://t.me/support_bot")],
                ]
            )
            await message.answer(support_text, reply_markup=keyboard)
        
        else:
            # Отправить общий ответ
            response_text = (
                "👋 Спасибо за сообщение!\n\n"
                "Доступные команды:\n"
                "/start - Начало\n"
                "/signals - Сигналы\n"
                "/vip - VIP подписка\n"
                "/profile - Профиль\n"
                "/balance - Баланс\n"
                "/help - Справка\n\n"
                "Используйте команды выше!"
            )
            await message.answer(response_text)
        
        logger.info(f"✅ Ответ отправлен пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_text: {e}", exc_info=True)
        await message.answer("❌ Произошла ошибка при обработке сообщения.")
