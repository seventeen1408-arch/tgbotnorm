"""
Скрипт для добавления тестовых данных в БД.
"""

import asyncio
from datetime import datetime, timedelta
from app.database.db import db
from app.core import config, setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def seed_data():
    """Добавить тестовые данные."""
    try:
        # Инициализировать БД
        await db.init()
        logger.info("✅ БД инициализирована")
        
        # Добавить казино
        casinos = [
            {
                "name": "Vavada",
                "url": "https://gate707.com/?promo=27893794-20bf-4a59-b4f2-c876a05720fb&target=register",
                "promo_code": "fulls"
            },
            {
                "name": "1Win",
                "url": "https://lkpq.cc/946678",
                "promo_code": "FULLS"
            }
        ]
        
        # Добавить сигналы
        signals = [
            {
                "game_name": "🛩️ Aviator",
                "coefficient": 2.5,
                "time_utc": "15:30",
                "is_vip_only": False,
                "casino": "Vavada",
                "recommended_bet": "100 ₽"
            },
            {
                "game_name": "⛏️ Mines",
                "coefficient": 3.0,
                "time_utc": "15:45",
                "is_vip_only": False,
                "casino": "1Win",
                "recommended_bet": "150 ₽"
            },
            {
                "game_name": "🎰 Book of Ra",
                "coefficient": 2.2,
                "time_utc": "16:00",
                "is_vip_only": True,
                "casino": "Vavada",
                "recommended_bet": "200 ₽"
            },
            {
                "game_name": "🎲 Dice",
                "coefficient": 1.8,
                "time_utc": "16:15",
                "is_vip_only": False,
                "casino": "1Win",
                "recommended_bet": "100 ₽"
            },
            {
                "game_name": "🎯 Crash",
                "coefficient": 2.8,
                "time_utc": "16:30",
                "is_vip_only": False,
                "casino": "Vavada",
                "recommended_bet": "250 ₽"
            },
            {
                "game_name": "🃏 Poker",
                "coefficient": 2.1,
                "time_utc": "16:45",
                "is_vip_only": True,
                "casino": "1Win",
                "recommended_bet": "300 ₽"
            },
            {
                "game_name": "🎪 Slots",
                "coefficient": 2.4,
                "time_utc": "17:00",
                "is_vip_only": False,
                "casino": "Vavada",
                "recommended_bet": "150 ₽"
            },
            {
                "game_name": "🎮 Game Show",
                "coefficient": 3.2,
                "time_utc": "17:15",
                "is_vip_only": True,
                "casino": "1Win",
                "recommended_bet": "200 ₽"
            }
        ]
        
        # Добавить сигналы в БД
        logger.info("📊 Добавляю сигналы...")
        for signal in signals:
            try:
                # Вставить сигнал в БД
                query = """
                INSERT INTO signals (game_name, coefficient, time_utc, is_vip_only, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """
                
                await db.execute(
                    query,
                    (
                        signal["game_name"],
                        signal["coefficient"],
                        signal["time_utc"],
                        signal["is_vip_only"],
                        datetime.utcnow()
                    )
                )
                
                logger.info(f"✅ Сигнал добавлен: {signal['game_name']}")
            except Exception as e:
                logger.error(f"❌ Ошибка при добавлении сигнала {signal['game_name']}: {e}")
        
        logger.info("✅ Все сигналы добавлены!")
        
        # Закрыть соединение
        await db.close()
        logger.info("✅ БД закрыта")
    
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(seed_data())
