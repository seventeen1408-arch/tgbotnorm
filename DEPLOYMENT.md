# Deployment Guide - GamblingBot PRO

Полная инструкция по развертыванию на Ubuntu VPS.

## 📋 Требования

- Ubuntu 20.04 LTS или выше
- Docker & Docker Compose установлены
- Доменное имя с SSL сертификатом
- Telegram Bot Token
- Минимум 2GB RAM, 10GB диска

## 🔧 Установка Docker & Docker Compose

### 1. Установить Docker

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
```

### 2. Установить Docker Compose

```bash
# Скачать Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Сделать исполняемым
sudo chmod +x /usr/local/bin/docker-compose

# Проверить установку
docker-compose --version
```

## 📦 Развертывание приложения

### 1. Клонировать репозиторий

```bash
# Создать директорию
mkdir -p /opt/gambling_bot
cd /opt/gambling_bot

# Клонировать репозиторий
git clone https://github.com/your-repo/gambling_bot_pro.git .
```

### 2. Настроить переменные окружения

```bash
# Скопировать пример
cp .env.example .env

# Отредактировать
nano .env
```

**Обязательно заполнить:**

```env
# Telegram Bot Token от @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ

# Ваш домен с https://
WEBHOOK_URL=https://your-domain.com

# Пароли для БД (сгенерировать)
DB_USER=gambling_user
DB_PASSWORD=your_strong_password_here
DB_NAME=gambling_bot

# Казино ссылки
CASINO_LINK_1=https://1win.uz/ref123
CASINO_LINK_2=https://vavada.uz/ref456
```

### 3. Настроить Nginx (обратный прокси)

Создать конфиг `/etc/nginx/sites-available/gambling_bot`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Редирект на HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL сертификаты (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL параметры
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Проксирование на бот
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Для вебхуков
        proxy_read_timeout 30s;
        proxy_connect_timeout 30s;
    }
}
```

Активировать конфиг:

```bash
sudo ln -s /etc/nginx/sites-available/gambling_bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Получить SSL сертификат (Let's Encrypt)

```bash
# Установить Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получить сертификат
sudo certbot certonly --nginx -d your-domain.com

# Автоматическое продление
sudo systemctl enable certbot.timer
```

### 5. Запустить приложение

```bash
cd /opt/gambling_bot

# Собрать и запустить контейнеры
docker compose up -d --build

# Проверить статус
docker compose ps

# Просмотреть логи
docker compose logs -f bot
```

## ✅ Проверка работы

### 1. Проверить healthcheck

```bash
curl https://your-domain.com/health
```

Ответ:
```json
{
  "status": "ok",
  "service": "gambling_bot_pro",
  "version": "2.0.0"
}
```

### 2. Проверить webhook в Telegram

```bash
curl -X POST https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo
```

Ответ должен содержать:
```json
{
  "ok": true,
  "result": {
    "url": "https://your-domain.com/webhook/{BOT_TOKEN}",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

### 3. Протестировать бота

Отправить команду боту в Telegram:
```
/start
```

Бот должен ответить приветствием.

## 🔍 Мониторинг

### Просмотр логов

```bash
# Логи бота
docker compose logs -f bot

# Логи PostgreSQL
docker compose logs -f postgres

# Логи Redis
docker compose logs -f redis

# Все логи
docker compose logs -f
```

### Проверка ресурсов

```bash
# Использование памяти и CPU
docker stats

# Размер контейнеров
docker system df
```

### Проверка БД

```bash
# Подключиться к PostgreSQL
docker compose exec postgres psql -U gambling_user -d gambling_bot

# Примеры команд:
SELECT COUNT(*) FROM users;
SELECT * FROM events LIMIT 10;
SELECT * FROM postbacks WHERE status='pending';
```

## 🔐 Безопасность

### 1. Firewall

```bash
# Установить UFW
sudo apt install ufw -y

# Разрешить SSH
sudo ufw allow 22/tcp

# Разрешить HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включить firewall
sudo ufw enable
```

### 2. Резервные копии

```bash
# Создать бэкап БД
docker compose exec postgres pg_dump -U gambling_user gambling_bot > backup_$(date +%Y%m%d).sql

# Восстановить из бэкапа
docker compose exec -T postgres psql -U gambling_user gambling_bot < backup_20260212.sql
```

### 3. Обновления

```bash
# Обновить образы
docker compose pull

# Пересобрать и перезагрузить
docker compose up -d --build
```

## 🚨 Troubleshooting

### Бот не отвечает

```bash
# Проверить логи
docker compose logs bot

# Перезагрузить контейнер
docker compose restart bot

# Проверить webhook
curl -X POST https://api.telegram.org/bot{BOT_TOKEN}/setWebhook \
  -d url=https://your-domain.com/webhook/{BOT_TOKEN}
```

### PostgreSQL не запускается

```bash
# Проверить логи
docker compose logs postgres

# Удалить и пересоздать
docker compose down -v
docker compose up -d --build
```

### Redis не подключается

```bash
# Проверить
docker compose exec redis redis-cli ping

# Перезагрузить
docker compose restart redis
```

### Webhook ошибки

```bash
# Проверить SSL
curl -v https://your-domain.com/health

# Проверить Nginx
sudo nginx -t
sudo systemctl restart nginx

# Проверить firewall
sudo ufw status
```

## 📊 Масштабирование

### Для большого трафика:

1. **Несколько инстансов бота:**
   - Настроить load balancer
   - Использовать Redis для shared state

2. **PostgreSQL репликация:**
   - Настроить master-slave
   - Использовать PgBouncer для connection pooling

3. **Redis Cluster:**
   - Для распределенного кэша
   - Для высокой доступности

## 📞 Поддержка

Для проблем:
1. Проверить логи
2. Проверить конфигурацию
3. Создать issue в репозитории

## 🎓 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

---

**Версия:** 2.0.0  
**Дата:** 2026-02-12
