"""
Конфигурация приложения.
Все параметры из переменных окружения.
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения."""
    
    # Telegram
    BOT_TOKEN: str
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/webhook"
    
    # Сервер
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # База данных
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/gambling_bot"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # CryptoBot
    CRYPTOBOT_TOKEN: Optional[str] = None
    
    # Казино ссылки
    CASINO_LINK_1: str = "https://1win.uz"
    CASINO_LINK_2: str = "https://vavada.uz"
    
    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/bot.log"
    
    # SoftGate параметры
    SOFT_GATE_CHECK_INTERVAL: int = 10  # секунды
    FREE_ACCESS_DURATION_MINUTES: int = 120  # 2 часа
    FREE_ACCESS_LIMIT_HOURS: int = 24  # 1 раз в 24 часа
    AUTO_UNLOCK_DURATION_HOURS: int = 24  # После депозита
    
    # Retention параметры
    RETENTION_CHECK_INTERVAL: int = 60  # секунды
    RETENTION_MESSAGES_INTERVAL: int = 3600  # 1 час
    
    # Postback параметры
    POSTBACK_SECRET: Optional[str] = None
    POSTBACK_TIMEOUT: int = 30  # секунды
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Инициализировать конфиг
config = Settings()


def validate_config() -> None:
    """Валидировать критические параметры."""
    required = ["BOT_TOKEN", "WEBHOOK_URL", "DATABASE_URL"]
    missing = [param for param in required if not getattr(config, param, None)]
    
    if missing:
        raise ValueError(f"Отсутствуют обязательные параметры: {', '.join(missing)}")
