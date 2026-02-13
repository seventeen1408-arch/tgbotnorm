# Quick Start - GamblingBot PRO

Запуск за 5 минут на Ubuntu VPS.

## 🚀 One-liner Deploy

```bash
# 1. Установить Docker
curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker $USER && newgrp docker

# 2. Установить Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose

# 3. Клонировать и запустить
git clone https://github.com/your-repo/gambling_bot_pro.git && cd gambling_bot_pro && cp .env.example .env && nano .env && docker compose up -d --build
```

## ✅ Минимальная конфигурация

Отредактировать `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
WEBHOOK_URL=https://your-domain.com
DB_PASSWORD=your_strong_password
CASINO_LINK_1=https://1win.uz/ref123
CASINO_LINK_2=https://vavada.uz/ref456
```

## 🔍 Проверка

```bash
# Статус контейнеров
docker compose ps

# Логи бота
docker compose logs -f bot

# Healthcheck
curl https://your-domain.com/health
```

## 📞 Команды

```bash
# Запустить
docker compose up -d --build

# Остановить
docker compose down

# Перезагрузить
docker compose restart bot

# Логи
docker compose logs -f bot

# Вход в контейнер
docker compose exec bot bash

# Проверить БД
docker compose exec postgres psql -U gambling_user -d gambling_bot -c "SELECT COUNT(*) FROM users;"
```

## 🎯 Что дальше?

1. ✅ Бот работает
2. ✅ Webhook настроен
3. ✅ БД готова
4. 📖 Читай [README.md](./README.md) для полной документации
5. 🔧 Читай [DEPLOYMENT.md](./DEPLOYMENT.md) для production setup

## 🆘 Проблемы?

```bash
# Проверить логи
docker compose logs bot

# Перезагрузить все
docker compose down -v && docker compose up -d --build

# Проверить webhook
curl -X POST https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo
```

---

**Версия:** 2.0.0
