"""
Логирование приложения.
Логи в консоль и файл.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import config


def setup_logging() -> None:
    """Настроить логирование."""
    # Создать директорию для логов
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    # Получить корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Обработчик файла
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Получить логгер по имени."""
    return logging.getLogger(name)
