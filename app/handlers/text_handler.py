"""
Обработчик текстовых сообщений.
"""

from aiogram import Router, F
from aiogram.types import Message
from app.core import get_logger
from app.database.db import db
from app.services.autoresponder_service import AutoResponderService

logger = get_logger(__name__)
router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    """Обработчик текстовых сообщений."""
    user_id = message.from_user.id
    text = message.text
    
    logger.info(f"💬 Сообщение от {user_id}: {text}")
    
    try:
        # Логировать событие
        await db.create_event(user_id, "message_received", text)
        
        # Отправить автоответ
        autoresponder = AutoResponderService(db)
        response = await autoresponder.send_auto_response(user_id, "help")
        await message.answer(response)
        logger.info(f"✅ Ответ отправлен пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_text: {e}", exc_info=True)
        await message.answer("❌ Произошла ошибка при обработке сообщения.")
