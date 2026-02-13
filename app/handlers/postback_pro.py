"""
Обработчик постбеков от казино.
"""

from fastapi import APIRouter, Request, HTTPException
from app.core import get_logger, config

logger = get_logger(__name__)
router = APIRouter()


async def setup_postback_routes(app, db, postback_service):
    """Настроить маршруты для постбеков."""
    
    @app.post("/postback/1win")
    async def handle_1win_postback(request: Request):
        """Обработчик постбеков от 1win."""
        try:
            data = await request.json()
            logger.info(f"📨 Постбек от 1win: {data}")
            
            # Обработать постбек
            user_id = data.get("user_id")
            event_type = data.get("event_type")
            amount = data.get("amount", 0)
            
            if user_id:
                await postback_service.process_postback(
                    user_id=user_id,
                    casino_id="1win",
                    event_type=event_type,
                    amount=amount,
                    raw_data=str(data)
                )
            
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"❌ Ошибка обработки постбека 1win: {e}")
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.post("/postback/vavada")
    async def handle_vavada_postback(request: Request):
        """Обработчик постбеков от Vavada."""
        try:
            data = await request.json()
            logger.info(f"📨 Постбек от Vavada: {data}")
            
            # Обработать постбек
            user_id = data.get("user_id")
            event_type = data.get("event_type")
            amount = data.get("amount", 0)
            
            if user_id:
                await postback_service.process_postback(
                    user_id=user_id,
                    casino_id="vavada",
                    event_type=event_type,
                    amount=amount,
                    raw_data=str(data)
                )
            
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"❌ Ошибка обработки постбека Vavada: {e}")
            raise HTTPException(status_code=400, detail=str(e))
