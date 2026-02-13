"""
Обработчик постбеков от казино.
"""

from aiogram import Router
from app.core import get_logger

logger = get_logger(__name__)
router = Router()


# Постбеки обрабатываются через FastAPI, не через aiogram
# Этот файл оставлен для совместимости
