"""
Обработчик команды /help.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.core import get_logger
from app.database.db import db

logger = get_logger(__name__)
router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    user_id = message.from_user.id
    
    logger.info(f"❓ Справка запрос от пользователя {user_id}")
    
    try:
        help_text = (
            "❓ **СПРАВКА И ПОМОЩЬ**\n\n"
            "**ОСНОВНЫЕ КОМАНДЫ:**\n"
            "/start - Начало работы\n"
            "/help - Эта справка\n"
            "/signals - Просмотр сигналов\n"
            "/vip - VIP подписка\n"
            "/profile - Мой профиль\n"
            "/balance - Мой баланс\n\n"
            "**КАК РАБОТАЕТ БОТ:**\n"
            "1. 📲 Отправьте /start для начала\n"
            "2. 📊 Используйте /signals для просмотра сигналов\n"
            "3. 💎 Получите VIP через /vip для полного доступа\n"
            "4. 💰 Отслеживайте баланс через /balance\n\n"
            "**ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ:**\n"
            "❓ Как получить сигналы?\n"
            "Используйте команду /signals\n\n"
            "❓ Как получить VIP?\n"
            "Используйте команду /vip\n\n"
            "❓ Как связаться с поддержкой?\n"
            "Нажмите кнопку ниже"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/support_bot")],
                [InlineKeyboardButton(text="📊 Сигналы", callback_data="signals")],
                [InlineKeyboardButton(text="💎 VIP", callback_data="vip_1month")],
            ]
        )
        
        await message.answer(help_text, reply_markup=keyboard)
        logger.info(f"✅ Справка отправлена пользователю {user_id}")
        
        # Логировать событие
        await db.create_event(user_id, "help_request")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_help: {e}", exc_info=True)
        await message.answer("❌ Ошибка при загрузке справки.")
