"""
Обработчик сигналов для игр.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.core import get_logger
from app.database.db import db
from app.services.soft_gate_service import SoftGateService

logger = get_logger(__name__)
router = Router()

# Казино с ссылками и промокодами
CASINOS = {
    "Vavada": {
        "url": "https://gate707.com/?promo=27893794-20bf-4a59-b4f2-c876a05720fb&target=register",
        "promo_code": "fulls"
    },
    "1Win": {
        "url": "https://lkpq.cc/946678",
        "promo_code": "FULLS"
    }
}


@router.message(Command("signals"))
async def cmd_signals(message: Message):
    """Обработчик команды /signals."""
    user_id = message.from_user.id
    
    logger.info(f"📊 Запрос сигналов от пользователя {user_id}")
    
    try:
        # Проверить доступ
        soft_gate = SoftGateService(db)
        has_access = await soft_gate.check_access(user_id)
        
        if not has_access:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💎 Получить VIP", callback_data="vip_subscribe")],
                    [InlineKeyboardButton(text="🎁 Бесплатный доступ", callback_data="free_access")],
                ]
            )
            await message.answer(
                "❌ У вас нет доступа к сигналам.\n\n"
                "💎 Приобретите VIP подписку или получите бесплатный доступ.",
                reply_markup=keyboard
            )
            return
        
        # Получить сигналы из БД
        signals = await db.get_signals()
        
        if not signals:
            await message.answer(
                "📊 Сигналов нет.\n\n"
                "Сигналы обновляются каждый час. Проверьте позже!"
            )
            return
        
        # Отправить сигналы с кнопками казино
        signals_text = "📊 **ДОСТУПНЫЕ СИГНАЛЫ**\n\n"
        
        for i, signal in enumerate(signals[:10], 1):  # Первые 10 сигналов
            game_name = signal.get('game_name', 'Unknown')
            coefficient = signal.get('coefficient', 'N/A')
            time_utc = signal.get('time_utc', 'N/A')
            is_vip = signal.get('is_vip_only', False)
            
            vip_badge = "💎 VIP" if is_vip else "✅ Бесплатно"
            
            signals_text += (
                f"{i}. {game_name}\n"
                f"   📈 Коэффициент: {coefficient}x\n"
                f"   ⏰ Время: {time_utc} UTC\n"
                f"   {vip_badge}\n\n"
            )
        
        await message.answer(signals_text)
        
        # Отправить кнопки казино
        casino_text = "🎰 **ВЫБЕРИТЕ КАЗИНО:**\n\n"
        
        keyboard_buttons = []
        for casino_name, casino_info in CASINOS.items():
            promo = casino_info.get('promo_code', '')
            button_text = f"🎰 {casino_name}"
            if promo:
                button_text += f" (промо: {promo})"
            
            keyboard_buttons.append(
                [InlineKeyboardButton(
                    text=button_text,
                    url=casino_info['url']
                )]
            )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await message.answer(casino_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "signal_view", f"Просмотрено {len(signals)} сигналов")
        logger.info(f"✅ Сигналы отправлены пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_signals: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении сигналов. Попробуйте позже.")


@router.message(F.text.contains("сигнал"))
async def handle_signals_text(message: Message):
    """Обработчик текстовых запросов о сигналах."""
    user_id = message.from_user.id
    
    logger.info(f"📊 Текстовый запрос сигналов от пользователя {user_id}")
    
    try:
        # Проверить доступ
        soft_gate = SoftGateService(db)
        has_access = await soft_gate.check_access(user_id)
        
        if not has_access:
            await message.answer(
                "❌ У вас нет доступа к сигналам.\n"
                "💎 Приобретите VIP подписку для получения сигналов.\n\n"
                "Используйте команду /vip для подробной информации."
            )
            return
        
        # Получить последний сигнал
        signals = await db.get_signals()
        
        if not signals:
            await message.answer("📊 Сигналов нет. Проверьте позже!")
            return
        
        signal = signals[0]  # Последний сигнал
        
        game_name = signal.get('game_name', 'Unknown')
        coefficient = signal.get('coefficient', 'N/A')
        time_utc = signal.get('time_utc', 'N/A')
        
        signal_text = (
            f"🎯 **Последний сигнал**\n\n"
            f"Игра: {game_name}\n"
            f"Коэффициент: {coefficient}x\n"
            f"Время: {time_utc} UTC\n\n"
            f"Используйте /signals для просмотра всех сигналов."
        )
        
        # Добавить кнопки казино
        keyboard_buttons = []
        for casino_name, casino_info in CASINOS.items():
            promo = casino_info.get('promo_code', '')
            button_text = f"🎰 {casino_name}"
            if promo:
                button_text += f" (промо: {promo})"
            
            keyboard_buttons.append(
                [InlineKeyboardButton(
                    text=button_text,
                    url=casino_info['url']
                )]
            )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await message.answer(signal_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "signal_request", game_name)
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_signals_text: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении сигнала.")


@router.message(F.text.contains("казино"))
async def handle_casino_request(message: Message):
    """Обработчик запросов о казино."""
    user_id = message.from_user.id
    
    logger.info(f"🎰 Запрос казино от пользователя {user_id}")
    
    try:
        casino_text = "🎰 **НАШИ КАЗИНО ПАРТНЕРЫ:**\n\n"
        
        keyboard_buttons = []
        for casino_name, casino_info in CASINOS.items():
            promo = casino_info.get('promo_code', '')
            
            casino_text += (
                f"🎰 **{casino_name}**\n"
                f"Промокод: {promo}\n"
                f"Перейти: {casino_info['url']}\n\n"
            )
            
            button_text = f"🎰 {casino_name}"
            if promo:
                button_text += f" (промо: {promo})"
            
            keyboard_buttons.append(
                [InlineKeyboardButton(
                    text=button_text,
                    url=casino_info['url']
                )]
            )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await message.answer(casino_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "casino_request", "Запрос информации о казино")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_casino_request: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении информации о казино.")
