"""
Локализация сообщений.
"""

MESSAGES = {
    "ru": {
        "start_welcome": "🎰 Добро пожаловать в SlotSignalsBot!\n\nПолучайте сигналы для игры в слоты.",
        "signals_available": "📊 Доступные сигналы:\n\n{signals}",
        "signal_locked": "🔒 Сигналы заблокированы. Разблокировка через {time}",
        "vip_required": "⭐ Для доступа требуется VIP подписка",
        "error": "❌ Произошла ошибка: {error}",
    }
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить переведенное сообщение."""
    message = MESSAGES.get(lang, {}).get(key, key)
    return message.format(**kwargs) if kwargs else message
