"""
Обработчик команды /start.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from app.core import get_logger
from app.database.db import db

logger = get_logger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    username = message.from_user.username
    
    logger.info(f"👤 Новый пользователь: {user_id} (@{username})")
    
    try:
        # Создать или получить пользователя
        user = await db.get_user(user_id)
        if not user:
            user = await db.create_user(user_id, username)
            logger.info(f"✅ Пользователь {user_id} создан в БД")
        
        # Отправить приветственное сообщение
        welcome_text = (
            "👋 Добро пожаловать в наш бот!\n\n"
            "📊 Здесь вы найдете:\n"
            "• 🎯 Точные сигналы для игр\n"
            "• 💎 VIP доступ к эксклюзивному контенту\n"
            "• 🎁 Ежедневные бонусы\n\n"
            "Выберите действие:"
        )
        
        await message.answer(welcome_text)
        logger.info(f"✅ Приветственное сообщение отправлено пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_start: {e}", exc_info=True)
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
