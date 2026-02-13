"""
Обработчик команды /start.
"""

from aiogram import Router, F
from aiogram.types import Message
from app.core import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(commands=["start"])
async def cmd_start(message: Message, db, bot):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    username = message.from_user.username
    
    logger.info(f"👤 Новый пользователь: {user_id} (@{username})")
    
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
