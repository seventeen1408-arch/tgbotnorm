#!/usr/bin/env python3
"""
Запуск FastAPI приложения с SSL поддержкой
"""

import uvicorn
import os
from pathlib import Path

# Пути к сертификатам
CERT_DIR = Path("/app/certs")
CERT_FILE = CERT_DIR / "tgbotlab.com.crt"
KEY_FILE = CERT_DIR / "tgbotlab.com.key"

# Проверить наличие сертификатов
if not CERT_FILE.exists() or not KEY_FILE.exists():
    print(f"❌ Сертификаты не найдены!")
    print(f"   Ожидается: {CERT_FILE} и {KEY_FILE}")
    print(f"   Запуск без SSL...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
else:
    print(f"✅ Сертификаты найдены")
    print(f"   Cert: {CERT_FILE}")
    print(f"   Key: {KEY_FILE}")
    
    # Запустить с SSL на порту 8443
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile=str(KEY_FILE),
        ssl_certfile=str(CERT_FILE),
        reload=False,
        log_level="info"
    )
