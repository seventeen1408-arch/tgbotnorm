# GamblingBot PRO - Production Version

Production-ready Telegram gambling arbitrage bot с webhook, PostgreSQL и Redis.

## 🎯 Особенности

- ✅ **Webhook режим** - вместо polling
- ✅ **FastAPI** - для обработки вебхуков и постбеков
- ✅ **PostgreSQL** - надежная база данных
- ✅ **Redis** - FSM storage и кэширование
- ✅ **Docker** - полная контейнеризация
- ✅ **APScheduler** - фоновые задачи
- ✅ **Healthcheck** - мониторинг здоровья

## 📋 Функциональность

### SoftGate (Управление доступом)
- 2 часа бесплатного доступа к сигналам
- 1 раз в 24 часа лимит
- Auto unlock при депозите (24 часа)
- FOMO countdown с напоминаниями
- VIP игнорирует лимиты

### Subscription (VIP система)
- Управление VIP подписками
- Автоматическое продление
- Разные уровни доступа

### AutoResponder (Автоответчик)
- Автоматические сообщения
- Retention сообщения
- Фоновые задачи

### Postback (Отслеживание конверсии)
- Получение постбеков от казино
- Обработка событий (deposit, withdrawal, bet, win)
- Отслеживание заработков

### Signals (Сигналы)
- Разные сигналы для VIP и обычных
- Управление доступом
- История сигналов

## 🚀 Быстрый старт

### Требования

- Docker & Docker Compose
- Ubuntu 20.04+ или другой Linux
- Telegram Bot Token (@BotFather)
- Доменное имя для webhook

### Установка

1. **Клонировать репозиторий:**
```bash
git clone https://github.com/your-repo/gambling_bot_pro.git
cd gambling_bot_pro
```

2. **Создать .env файл:**
```bash
cp .env.example .env
```

3. **Отредактировать .env:**
```bash
nano .env
```

Обязательные параметры:
- `BOT_TOKEN` - токен от @BotFather
- `WEBHOOK_URL` - ваш домен (https://your-domain.com)
- `DATABASE_URL` - будет автоматически (postgres:5432)
- `REDIS_URL` - будет автоматически (redis:6379)

4. **Запустить приложение:**
```bash
docker compose up -d --build
```

5. **Проверить статус:**
```bash
docker compose ps
docker compose logs -f bot
```

## 📝 Конфигурация

### Переменные окружения

```env
# Telegram
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com
WEBHOOK_PATH=/webhook

# Сервер
HOST=0.0.0.0
PORT=8000

# База данных
DATABASE_URL=postgresql://user:password@postgres:5432/gambling_bot
REDIS_URL=redis://redis:6379/0

# Казино ссылки
CASINO_LINK_1=https://1win.uz
CASINO_LINK_2=https://vavada.uz

# Логирование
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# SoftGate
SOFT_GATE_CHECK_INTERVAL=10
FREE_ACCESS_DURATION_MINUTES=120
FREE_ACCESS_LIMIT_HOURS=24
AUTO_UNLOCK_DURATION_HOURS=24

# Retention
RETENTION_CHECK_INTERVAL=60
RETENTION_MESSAGES_INTERVAL=3600

# Postback
POSTBACK_SECRET=your_postback_secret
POSTBACK_TIMEOUT=30
```

## 🔧 Управление

### Запуск
```bash
docker compose up -d --build
```

### Остановка
```bash
docker compose down
```

### Просмотр логов
```bash
docker compose logs -f bot
```

### Перезагрузка
```bash
docker compose restart bot
```

### Вход в контейнер
```bash
docker compose exec bot bash
```

## 📊 API Endpoints

### Healthcheck
```bash
GET /health
```

Ответ:
```json
{
  "status": "ok",
  "service": "gambling_bot_pro",
  "version": "2.0.0"
}
```

### Webhook Telegram
```bash
POST /webhook/{BOT_TOKEN}
```

### Postback от казино
```bash
POST /postback/{casino_id}
```

## 🗄️ База данных

### Таблицы

- `users` - пользователи
- `signals` - сигналы
- `postbacks` - постбеки от казино
- `events` - события пользователя
- `subscriptions` - подписки
- `payments` - платежи

### Подключение к БД

```bash
docker compose exec postgres psql -U gambling_user -d gambling_bot
```

## 📦 Структура проекта

```
.
├── app/
│   ├── core/
│   │   ├── config.py      # Конфигурация
│   │   ├── logger.py      # Логирование
│   │   └── __init__.py
│   ├── database/
│   │   ├── db.py          # Работа с БД
│   │   ├── models.py      # Модели SQLAlchemy
│   │   └── __init__.py
│   ├── handlers/
│   │   ├── start.py       # /start команда
│   │   ├── signals.py     # /signals команда
│   │   ├── text_handler.py # Обработка текста
│   │   ├── vip_upsell.py  # VIP продажи
│   │   ├── postback_pro.py # Постбеки
│   │   └── __init__.py
│   ├── services/
│   │   ├── subscription.py         # VIP подписки
│   │   ├── soft_gate_service.py    # Управление доступом
│   │   ├── autoresponder_service.py # Автоответчик
│   │   ├── retention_service.py    # Retention
│   │   ├── postback_pro_service.py # Постбеки
│   │   └── __init__.py
│   ├── locales/
│   │   ├── i18n.py        # Локализация
│   │   └── __init__.py
│   └── __init__.py
├── migrations/
│   └── 001_init_schema.sql # Миграции БД
├── logs/                   # Логи приложения
├── main.py                 # Точка входа (FastAPI + Webhook)
├── requirements.txt        # Python зависимости
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Оркестрация сервисов
├── .env.example            # Пример конфигурации
└── README.md               # Этот файл
```

## 🐛 Troubleshooting

### Бот не отвечает

1. Проверить логи:
```bash
docker compose logs -f bot
```

2. Проверить webhook:
```bash
curl https://your-domain.com/health
```

3. Проверить БД:
```bash
docker compose exec postgres psql -U gambling_user -d gambling_bot -c "SELECT COUNT(*) FROM users;"
```

### PostgreSQL не запускается

```bash
docker compose logs postgres
docker compose down -v  # Удалить volumes
docker compose up -d --build
```

### Redis не подключается

```bash
docker compose exec redis redis-cli ping
docker compose restart redis
```

## 📞 Поддержка

Для вопросов и проблем создавайте issues в репозитории.

## 📄 Лицензия

Proprietary - Все права защищены.

## 🔐 Безопасность

- Все пароли в .env (не коммитить!)
- HTTPS для webhook
- Валидация постбеков
- Логирование всех операций
- Healthcheck для мониторинга

## 📈 Масштабирование

Для масштабирования:

1. Добавить load balancer (nginx)
2. Несколько инстансов бота
3. Настроить Redis для shared state
4. Настроить PostgreSQL репликацию

## 🎓 Документация

- [SoftGate Guide](./AUTO_FUNNEL_INTEGRATION.md)
- [Postback Guide](./POSTBACK_PRO_GUIDE.md)
- [AutoResponder Guide](./AUTORESPONDER_RETENTION_GUIDE.md)

---

**Версия:** 2.0.0  
**Последнее обновление:** 2026-02-12
