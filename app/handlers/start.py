"""
Обработчик команды /start.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.core import get_logger
from app.database.db import db

logger = get_logger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    
    logger.info(f"👋 Новый пользователь: {user_id} (@{username})")
    
    try:
        # Создать или получить пользователя
        user = await db.get_user(user_id)
        if not user:
            user = await db.create_user(user_id, username)
            logger.info(f"✅ Пользователь {user_id} создан в БД")
        
        # Приветственное сообщение
        welcome_text = (
            "👋 **Добро пожаловать в наш бот!**\n\n"
            "📊 Здесь вы найдете:\n"
            "• 🎯 Точные сигналы для игр\n"
            "• 💎 VIP доступ к эксклюзивному контенту\n"
            "• 🎁 Ежедневные бонусы\n\n"
            "**Выберите действие:**"
        )
        
        # Кнопки меню
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📊 Сигналы", callback_data="menu_signals")],
                [InlineKeyboardButton(text="🎰 Казино", callback_data="menu_casino")],
                [InlineKeyboardButton(text="💎 VIP Подписка", callback_data="menu_vip")],
                [InlineKeyboardButton(text="❓ Помощь", callback_data="menu_help")],
            ]
        )
        
        await message.answer(welcome_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "start", "Пользователь запустил бот")
        logger.info(f"✅ /start выполнена для пользователя {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в cmd_start: {e}", exc_info=True)
        await message.answer("❌ Ошибка при запуске бота. Попробуйте позже.")


@router.callback_query(F.data == "menu_signals")
async def callback_menu_signals(query: CallbackQuery):
    """Обработчик кнопки Сигналы."""
    user_id = query.from_user.id
    
    logger.info(f"📊 Пользователь {user_id} выбрал Сигналы")
    
    try:
        # Проверить доступ
        user = await db.get_user(user_id)
        
        if not user or not user.get('is_vip'):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💎 Получить VIP", callback_data="menu_vip")],
                    [InlineKeyboardButton(text="🎁 Бесплатный доступ", callback_data="free_access")],
                    [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
                ]
            )
            await query.message.edit_text(
                "❌ **У вас нет доступа к сигналам.**\n\n"
                "💎 Приобретите VIP подписку или получите бесплатный доступ.",
                reply_markup=keyboard
            )
            return
        
        # Получить сигналы из БД
        signals = await db.get_signals()
        
        if not signals:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
                ]
            )
            await query.message.edit_text(
                "📊 **Сигналов нет.**\n\n"
                "Сигналы обновляются каждый час. Проверьте позже!",
                reply_markup=keyboard
            )
            return
        
        # Отправить сигналы
        signals_text = "📊 **ДОСТУПНЫЕ СИГНАЛЫ**\n\n"
        
        for i, signal in enumerate(signals[:10], 1):
            game_name = signal.get('game_name', 'Unknown')
            coefficient = signal.get('coefficient', 'N/A')
            time_utc = signal.get('time_utc', 'N/A')
            
            signals_text += (
                f"{i}. {game_name}\n"
                f"   📈 Коэффициент: {coefficient}x\n"
                f"   ⏰ Время: {time_utc} UTC\n\n"
            )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎰 Перейти в казино", callback_data="menu_casino")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
            ]
        )
        
        await query.message.edit_text(signals_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "signals_view", f"Просмотрено {len(signals)} сигналов")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_menu_signals: {e}", exc_info=True)
        await query.answer("❌ Ошибка при получении сигналов.", show_alert=True)


@router.callback_query(F.data == "menu_casino")
async def callback_menu_casino(query: CallbackQuery):
    """Обработчик кнопки Казино."""
    user_id = query.from_user.id
    
    logger.info(f"🎰 Пользователь {user_id} выбрал Казино")
    
    try:
        casino_text = "🎰 **НАШИ КАЗИНО ПАРТНЕРЫ**\n\n"
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎰 Vavada (промо: fulls)", callback_data="casino_vavada")],
                [InlineKeyboardButton(text="🎰 1Win (промо: FULLS)", callback_data="casino_1win")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
            ]
        )
        
        await query.message.edit_text(casino_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "casino_view", "Просмотрено казино")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_menu_casino: {e}", exc_info=True)
        await query.answer("❌ Ошибка при получении информации о казино.", show_alert=True)


@router.callback_query(F.data == "casino_vavada")
async def callback_casino_vavada(query: CallbackQuery):
    """Обработчик кнопки Vavada."""
    user_id = query.from_user.id
    
    logger.info(f"🎰 Пользователь {user_id} выбрал Vavada")
    
    try:
        casino_text = (
            "🎰 **VAVADA**\n\n"
            "💳 Промокод: **fulls**\n"
            "🎁 Бонус: Приветственный пакет\n"
            "⚡ Быстрая регистрация\n\n"
            "Используйте промокод при регистрации!"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Перейти на Vavada", url="https://gate707.com/?promo=27893794-20bf-4a59-b4f2-c876a05720fb&target=register")],
                [InlineKeyboardButton(text="◀️ Назад к казино", callback_data="menu_casino")],
            ]
        )
        
        await query.message.edit_text(casino_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "casino_click", "Vavada")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_casino_vavada: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "casino_1win")
async def callback_casino_1win(query: CallbackQuery):
    """Обработчик кнопки 1Win."""
    user_id = query.from_user.id
    
    logger.info(f"🎰 Пользователь {user_id} выбрал 1Win")
    
    try:
        casino_text = (
            "🎰 **1WIN**\n\n"
            "💳 Промокод: **FULLS**\n"
            "🎁 Бонус: До 500% на первый депозит\n"
            "⚡ Быстрая регистрация\n\n"
            "Используйте промокод при регистрации!"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Перейти на 1Win", url="https://lkpq.cc/946678")],
                [InlineKeyboardButton(text="◀️ Назад к казино", callback_data="menu_casino")],
            ]
        )
        
        await query.message.edit_text(casino_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "casino_click", "1Win")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_casino_1win: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "menu_vip")
async def callback_menu_vip(query: CallbackQuery):
    """Обработчик кнопки VIP."""
    user_id = query.from_user.id
    
    logger.info(f"💎 Пользователь {user_id} выбрал VIP")
    
    try:
        vip_text = (
            "💎 **VIP ПОДПИСКА**\n\n"
            "📊 Получите доступ к:\n"
            "• 🎯 Приватным сигналам\n"
            "• 📈 Анализу коэффициентов\n"
            "• 🎁 Ежедневным бонусам\n"
            "• 👥 Приватной группе\n\n"
            "💰 **Цена: 1500 ₽**\n"
            "📅 **Период: 1 месяц**\n"
            "⏱️ **Длительность: 30 дней**"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить VIP", callback_data="vip_pay")],
                [InlineKeyboardButton(text="❓ Как оплатить?", callback_data="vip_help")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
            ]
        )
        
        await query.message.edit_text(vip_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "vip_view", "Просмотрено VIP")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_menu_vip: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "vip_pay")
async def callback_vip_pay(query: CallbackQuery):
    """Обработчик оплаты VIP."""
    user_id = query.from_user.id
    
    logger.info(f"💳 Пользователь {user_id} инициировал оплату VIP")
    
    try:
        pay_text = (
            "💳 **ОПЛАТА VIP ПОДПИСКИ**\n\n"
            "💰 Сумма: 1500 ₽\n"
            "📅 Период: 1 месяц\n"
            "⏱️ Длительность: 30 дней\n\n"
            "✅ Способы оплаты:\n"
            "• 💳 Карта (Visa/MasterCard)\n"
            "• 🏦 Банковский перевод\n"
            "• 📱 Мобильный платеж\n\n"
            "📞 Для оплаты свяжитесь с администратором."
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👨‍💼 Написать администратору", callback_data="admin_contact")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_vip")],
            ]
        )
        
        await query.message.edit_text(pay_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "vip_payment_init", "Инициирована оплата VIP")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_vip_pay: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "admin_contact")
async def callback_admin_contact(query: CallbackQuery):
    """Обработчик контакта администратора."""
    user_id = query.from_user.id
    
    logger.info(f"👨‍💼 Пользователь {user_id} запросил контакт администратора")
    
    try:
        admin_text = (
            "👨‍💼 **АДМИНИСТРАТОР**\n\n"
            "Для оплаты VIP подписки или вопросов:\n\n"
            "💬 Telegram: @admin_bot\n"
            "📧 Email: admin@example.com\n\n"
            "Мы ответим вам в течение 5 минут!"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💬 Написать администратору", url="https://t.me/admin_bot")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_vip")],
            ]
        )
        
        await query.message.edit_text(admin_text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_admin_contact: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "menu_help")
async def callback_menu_help(query: CallbackQuery):
    """Обработчик кнопки Помощь."""
    user_id = query.from_user.id
    
    logger.info(f"❓ Пользователь {user_id} выбрал Помощь")
    
    try:
        help_text = (
            "❓ **ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ**\n\n"
            "❓ **Как получить сигналы?**\n"
            "Приобретите VIP подписку или получите бесплатный доступ.\n\n"
            "❓ **Как оплатить VIP?**\n"
            "Свяжитесь с администратором через кнопку выше.\n\n"
            "❓ **Какие казино доступны?**\n"
            "Vavada и 1Win с промокодами.\n\n"
            "❓ **Как использовать промокод?**\n"
            "При регистрации введите промокод в поле \"Промокод\"."
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
            ]
        )
        
        await query.message.edit_text(help_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "help_view", "Просмотрена справка")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_menu_help: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "menu_back")
async def callback_menu_back(query: CallbackQuery):
    """Обработчик кнопки Назад."""
    user_id = query.from_user.id
    
    logger.info(f"◀️ Пользователь {user_id} вернулся в главное меню")
    
    try:
        welcome_text = (
            "👋 **Добро пожаловать в наш бот!**\n\n"
            "📊 Здесь вы найдете:\n"
            "• 🎯 Точные сигналы для игр\n"
            "• 💎 VIP доступ к эксклюзивному контенту\n"
            "• 🎁 Ежедневные бонусы\n\n"
            "**Выберите действие:**"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📊 Сигналы", callback_data="menu_signals")],
                [InlineKeyboardButton(text="🎰 Казино", callback_data="menu_casino")],
                [InlineKeyboardButton(text="💎 VIP Подписка", callback_data="menu_vip")],
                [InlineKeyboardButton(text="❓ Помощь", callback_data="menu_help")],
            ]
        )
        
        await query.message.edit_text(welcome_text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_menu_back: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)


@router.callback_query(F.data == "free_access")
async def callback_free_access(query: CallbackQuery):
    """Обработчик бесплатного доступа."""
    user_id = query.from_user.id
    
    logger.info(f"🎁 Пользователь {user_id} получил бесплатный доступ")
    
    try:
        # Дать бесплатный доступ на 24 часа
        await db.unlock_signals(user_id, hours=24)
        
        free_text = (
            "🎁 **БЕСПЛАТНЫЙ ДОСТУП АКТИВИРОВАН!**\n\n"
            "✅ Вы получили доступ к сигналам на 24 часа.\n\n"
            "📊 Используйте команду /signals для просмотра сигналов."
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📊 Просмотреть сигналы", callback_data="menu_signals")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_back")],
            ]
        )
        
        await query.message.edit_text(free_text, reply_markup=keyboard)
        
        # Логировать событие
        await db.create_event(user_id, "free_access_granted", "Бесплатный доступ на 24 часа")
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_free_access: {e}", exc_info=True)
        await query.answer("❌ Ошибка при активации доступа.", show_alert=True)


@router.callback_query(F.data == "vip_help")
async def callback_vip_help(query: CallbackQuery):
    """Обработчик справки по VIP."""
    user_id = query.from_user.id
    
    logger.info(f"❓ Пользователь {user_id} запросил справку по VIP")
    
    try:
        help_text = (
            "❓ **КАК ОПЛАТИТЬ VIP?**\n\n"
            "1️⃣ Нажмите кнопку \"Оплатить VIP\"\n"
            "2️⃣ Выберите способ оплаты\n"
            "3️⃣ Следуйте инструкциям\n"
            "4️⃣ Получите доступ сразу после оплаты\n\n"
            "💰 **Цена: 1500 ₽**\n"
            "📅 **Период: 1 месяц**"
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить VIP", callback_data="vip_pay")],
                [InlineKeyboardButton(text="◀️ Назад", callback_data="menu_vip")],
            ]
        )
        
        await query.message.edit_text(help_text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"❌ Ошибка в callback_vip_help: {e}", exc_info=True)
        await query.answer("❌ Ошибка.", show_alert=True)
