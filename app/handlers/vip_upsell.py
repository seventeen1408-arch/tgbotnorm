"""
Обработчик VIP функций и апсела.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.core import get_logger
from app.database.db import db

logger = get_logger(__name__)
router = Router()


class VIPStates(StatesGroup):
    """Состояния для VIP процесса."""
    waiting_for_payment = State()
    waiting_for_confirmation = State()


@router.message(Command("vip"))
async def cmd_vip(message: Message):
    """Обработчик команды /vip."""
    user_id = message.from_user.id
    
    logger.info(f"💎 VIP запрос от пользователя {user_id}")
    
    try:
        # Получить информацию о пользователе
        user = await db.get_user(user_id)
        
        vip_text = (
            "💎 **VIP ПОДПИСКА**\n\n"
            "Получите доступ к эксклюзивным функциям:\n\n"
            "✅ Все сигналы без ограничений\n"
            "✅ Приоритетная поддержка\n"
            "✅ Ежедневные бонусы\n"
            "✅ Ранний доступ к новым сигналам\n"
            "✅ Статистика и аналитика\n\n"
            "💰 **ЦЕНЫ:**\n"
            "• 1 месяц: 99 ₽\n"
            "• 3 месяца: 249 ₽ (скидка 16%)\n"
            "• 12 месяцев: 799 ₽ (скидка 33%)\n\n"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="1 месяц - 99₽", callback_data="vip_1month")],
                [InlineKeyboardButton(text="3 месяца - 249₽", callback_data="vip_3months")],
                [InlineKeyboardButton(text="12 месяцев - 799₽", callback_data="vip_12months")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
            ]
        )
        
        await message.answer(vip_text, reply_markup=keyboard)
        logger.info(f"✅ VIP меню отправлено пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_vip: {e}", exc_info=True)
        await message.answer("❌ Ошибка при загрузке VIP информации.")


@router.callback_query(F.data.startswith("vip_"))
async def handle_vip_callback(query: CallbackQuery, state: FSMContext):
    """Обработчик VIP callback кнопок."""
    user_id = query.from_user.id
    data = query.data
    
    logger.info(f"💎 VIP callback: {data} от пользователя {user_id}")
    
    try:
        if data == "cancel":
            await query.message.edit_text("❌ Отменено.")
            return
        
        # Определить период
        periods = {
            "vip_1month": ("1 месяц", 99, 30),
            "vip_3months": ("3 месяца", 249, 90),
            "vip_12months": ("12 месяцев", 799, 365),
        }
        
        if data not in periods:
            return
        
        period_name, price, days = periods[data]
        
        # Создать платеж
        payment_text = (
            f"💳 **ОПЛАТА VIP ПОДПИСКИ**\n\n"
            f"Период: {period_name}\n"
            f"Цена: {price} ₽\n"
            f"Длительность: {days} дней\n\n"
            f"⚠️ В этой версии платежи не интегрированы.\n"
            f"Пожалуйста, свяжитесь с поддержкой для оплаты.\n\n"
            f"📞 Поддержка: @support_bot"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📞 Связаться с поддержкой", url="https://t.me/support_bot")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
            ]
        )
        
        await query.message.edit_text(payment_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "vip_request", f"Запрос VIP: {period_name}")
        logger.info(f"✅ VIP запрос обработан: {period_name}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_vip_callback: {e}", exc_info=True)
        await query.message.edit_text("❌ Ошибка при обработке запроса.")


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Обработчик команды /profile."""
    user_id = message.from_user.id
    
    logger.info(f"👤 Профиль запрос от пользователя {user_id}")
    
    try:
        # Получить информацию о пользователе
        user = await db.get_user(user_id)
        
        profile_text = (
            f"👤 **МОЙ ПРОФИЛЬ**\n\n"
            f"ID: {user_id}\n"
            f"Имя: {message.from_user.first_name}\n"
            f"Юзернейм: @{message.from_user.username or 'не указан'}\n\n"
            f"📊 **СТАТИСТИКА:**\n"
            f"Статус: Обычный пользователь\n"
            f"Баланс: 0 ₽\n"
            f"Сигналов просмотрено: 0\n"
            f"Дата регистрации: сегодня\n"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💎 Получить VIP", callback_data="vip_1month")],
                [InlineKeyboardButton(text="📊 Мои сигналы", callback_data="my_signals")],
                [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
            ]
        )
        
        await message.answer(profile_text, reply_markup=keyboard)
        logger.info(f"✅ Профиль отправлен пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_profile: {e}", exc_info=True)
        await message.answer("❌ Ошибка при загрузке профиля.")


@router.message(Command("balance"))
async def cmd_balance(message: Message):
    """Обработчик команды /balance."""
    user_id = message.from_user.id
    
    logger.info(f"💰 Баланс запрос от пользователя {user_id}")
    
    try:
        balance_text = (
            "💰 **МОЙ БАЛАНС**\n\n"
            "Основной баланс: 0 ₽\n"
            "Бонусный баланс: 0 ₽\n"
            "Всего: 0 ₽\n\n"
            "📈 История транзакций пуста.\n\n"
            "💎 Пополните баланс через VIP подписку!"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💎 Получить VIP", callback_data="vip_1month")],
                [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/support_bot")],
            ]
        )
        
        await message.answer(balance_text, reply_markup=keyboard)
        logger.info(f"✅ Баланс отправлен пользователю {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_balance: {e}", exc_info=True)
        await message.answer("❌ Ошибка при загрузке баланса.")
