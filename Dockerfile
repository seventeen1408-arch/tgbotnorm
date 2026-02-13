# Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app

# Установить зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Скопировать requirements
COPY requirements.txt .

# Установить Python зависимости
RUN pip install --no-cache-dir --user -r requirements.txt


# Final stage
FROM python:3.11-slim

WORKDIR /app

# Установить runtime зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Скопировать Python пакеты из builder
COPY --from=builder /root/.local /root/.local

# Установить PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Скопировать приложение
COPY . .

# Создать директорию для логов
RUN mkdir -p logs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Запустить приложение с SSL
CMD ["python", "run_ssl.py"]
