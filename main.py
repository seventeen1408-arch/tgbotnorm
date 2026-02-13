"""
PRO-бот для арбитража трафика - Production версия.
Webhook + FastAPI + PostgreSQL + Redis
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from app.core import config, setup_logging, get_logger, validate_config
from app.database.db import db
from app.services.subscription import SubscriptionService
from app.services.soft_gate_service import SoftGateService
from app.services.autoresponder_service import AutoResponderService
from app.services.retention_service import RetentionService
from app.services.postback_pro_service import PostbackProService
from app.handlers import start, signals, text_handler, vip_upsell, postback_pro, help

# Настроить логирование
setup_logging()
logger = get_logger(__name__)

# Глобальные переменные
bot: Bot = None
dp: Dispatcher = None
scheduler: AsyncIOScheduler = None


async def on_startup() -> None:
    """Инициализация при запуске."""
    global bot, dp, scheduler
    
    try:
        logger.info("=" * 60)
        logger.info("🚀 Запуск PRO-бота для арбитража трафика...")
        logger.info("=" * 60)
        
        # Инициализировать БД
        await db.init()
        logger.info("✅ PostgreSQL инициализирована")
        
        # Инициализировать Redis
        redis_storage = RedisStorage.from_url(config.REDIS_URL)
        logger.info("✅ Redis инициализирован")
        
        # Создать бота
        bot = Bot(token=config.BOT_TOKEN)
        logger.info("✅ Бот инициализирован")
        
        # Создать диспетчер
        dp = Dispatcher(storage=redis_storage)
        
        # Создать сервисы
        subscription_service = SubscriptionService(db)
        soft_gate_service = SoftGateService(db)
        autoresponder_service = AutoResponderService(db)
        retention_service = RetentionService(db)
        postback_pro_service = PostbackProService(db)
        
        # Сохранить сервисы в контекст
        dp.workflow_data["subscription_service"] = subscription_service
        dp.workflow_data["soft_gate_service"] = soft_gate_service
        dp.workflow_data["autoresponder_service"] = autoresponder_service
        dp.workflow_data["retention_service"] = retention_service
        dp.workflow_data["postback_pro_service"] = postback_pro_service
        
        logger.info("✅ Сервисы инициализированы")
        
        # Регистрировать роутеры
        dp.include_router(start.router)
        dp.include_router(help.router)
        dp.include_router(signals.router)
        dp.include_router(vip_upsell.router)
        dp.include_router(text_handler.router)
        dp.include_router(postback_pro.router)
        
        logger.info("✅ Роутеры зарегистрированы")
        
        # Запустить планировщик
        scheduler = AsyncIOScheduler()
        
        scheduler.add_job(
            soft_gate_service.check_and_unlock_signals,
            "interval",
            seconds=config.SOFT_GATE_CHECK_INTERVAL,
            id="check_unlock_signals"
        )
        
        scheduler.add_job(
            retention_service.check_and_send_retention,
            "interval",
            seconds=config.RETENTION_CHECK_INTERVAL,
            id="check_retention"
        )
        
        scheduler.start()
        dp.workflow_data["scheduler"] = scheduler
        
        logger.info("✅ Планировщик запущен")
        
        # Использовать polling вместо webhook
        logger.info("✅ Бот работает в режиме polling")
        logger.info("📡 Запуск polling для получения обновлений...")
        
        # Запустить polling в фоне
        asyncio.create_task(dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()))
        
        logger.info("=" * 60)
        logger.info("✅ БОТ ГОТОВ К РАБОТЕ!")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации: {e}", exc_info=True)
        raise


async def on_shutdown() -> None:
    """Завершение при остановке."""
    try:
        logger.info("🛑 Остановка бота...")
        
        # Удалить webhook если был установлен
        if bot:
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                logger.info("✅ Webhook удален")
            except Exception:
                pass
        
        if scheduler:
            scheduler.shutdown()
            logger.info("✅ Планировщик остановлен")
        
        if bot:
            await bot.session.close()
            logger.info("✅ Сессия бота закрыта")
        
        logger.info("✅ Бот остановлен корректно")
    
    except Exception as e:
        logger.error(f"❌ Ошибка при остановке: {e}", exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения."""
    # Startup
    await on_startup()
    yield
    # Shutdown
    await on_shutdown()


# Создать FastAPI приложение
app = FastAPI(
    title="GamblingBot PRO",
    description="Production-ready gambling arbitrage bot",
    version="2.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения."""
    return {
        "status": "ok",
        "service": "gambling_bot_pro",
        "version": "2.0.0"
    }


@app.post(f"/webhook/{config.BOT_TOKEN}")
async def webhook(request: Request):
    """Получить обновление от Telegram."""
    try:
        update_data = await request.json()
        update = Update(**update_data)
        
        # Обработать обновление
        await dp.feed_update(bot, update)
        
        return JSONResponse({"ok": True})
    
    except Exception as e:
        logger.error(f"❌ Ошибка обработки webhook: {e}", exc_info=True)
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.post("/postback/{casino_id}")
async def postback_handler(casino_id: str, request: Request):
    """Получить постбек от казино."""
    try:
        postback_data = await request.json()
        
        # Получить сервис постбеков
        postback_service = dp.workflow_data.get("postback_pro_service")
        if not postback_service:
            return JSONResponse({"ok": False, "error": "Service not available"}, status_code=503)
        
        # Обработать постбек
        result = await postback_service.process_postback(casino_id, postback_data)
        
        return {"ok": True, "result": result}
    
    except Exception as e:
        logger.error(f"❌ Ошибка обработки постбека: {e}", exc_info=True)
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.on_event("startup")
async def startup():
    """Инициализация при запуске FastAPI."""
    global bot
    
    # Валидировать конфиг
    validate_config()
    
    # Создать бота
    bot = Bot(token=config.BOT_TOKEN)


@app.on_event("shutdown")
async def shutdown():
    """Завершение при остановке FastAPI."""
    if bot:
        await bot.session.close()


if __name__ == "__main__":
    import uvicorn
    
    # Запустить сервер
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=False,
        log_level=config.LOG_LEVEL.lower()
    )
