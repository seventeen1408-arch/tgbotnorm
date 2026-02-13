"""
Обработчик текстовых сообщений.
"""

from aiogram import Router, F
from aiogram.types import Message
from app.core import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(F.text)
async def handle_text(message: Message, db, autoresponder_service):
    """Обработчик текстовых сообщений."""
    user_id = message.from_user.id
    text = message.text
    
    logger.info(f"💬 Сообщение от {user_id}: {text}")
    
    # Логировать событие
    await db.create_event(user_id, "message_received", text)
    
    # Отправить автоответ
    response = await autoresponder_service.send_auto_response(user_id, "help")
    await message.answer(response)
