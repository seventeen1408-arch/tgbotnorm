"""
Класс для работы с базой данных.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core import config, get_logger
from app.database.models import Base, User, Signal, Postback, Event, Subscription

logger = get_logger(__name__)


class Database:
    """Класс для работы с базой данных."""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
        self.session_factory = None
    
    async def init(self):
        """Инициализировать подключение к БД."""
        try:
            # Создать асинхронный движок
            self.engine = create_async_engine(
                config.DATABASE_URL,
                echo=False,
                pool_size=20,
                max_overflow=0,
                pool_pre_ping=True
            )
            
            # Создать фабрику сессий
            self.async_session = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Создать таблицы
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("✅ База данных инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации БД: {e}")
            raise
    
    async def close(self):
        """Закрыть подключение к БД."""
        if self.engine:
            await self.engine.dispose()
            logger.info("✅ Подключение к БД закрыто")
    
    async def get_session(self) -> AsyncSession:
        """Получить сессию БД."""
        return self.async_session()
    
    # ===== User методы =====
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        async with self.async_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            return result.scalars().first()
    
    async def create_user(self, user_id: int, username: Optional[str] = None) -> User:
        """Создать нового пользователя."""
        async with self.async_session() as session:
            user = User(user_id=user_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Обновить пользователя."""
        async with self.async_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalars().first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                await session.commit()
                await session.refresh(user)
            return user
    
    # ===== Signal методы =====
    
    async def get_signals(self, vip_only: bool = False) -> List[Signal]:
        """Получить сигналы."""
        async with self.async_session() as session:
            query = select(Signal)
            if vip_only:
                query = query.where(Signal.is_vip_only == True)
            result = await session.execute(query)
            return result.scalars().all()
    
    async def create_signal(self, game_name: str, coefficient: float, 
                           time_utc: str, is_vip_only: bool = False) -> Signal:
        """Создать сигнал."""
        async with self.async_session() as session:
            signal = Signal(
                game_name=game_name,
                coefficient=coefficient,
                time_utc=time_utc,
                is_vip_only=is_vip_only
            )
            session.add(signal)
            await session.commit()
            await session.refresh(signal)
            return signal
    
    # ===== Postback методы =====
    
    async def create_postback(self, user_id: int, casino_id: str, 
                             event_type: str, amount: float, raw_data: str) -> Postback:
        """Создать постбек."""
        async with self.async_session() as session:
            postback = Postback(
                user_id=user_id,
                casino_id=casino_id,
                event_type=event_type,
                amount=amount,
                status="pending",
                raw_data=raw_data
            )
            session.add(postback)
            await session.commit()
            await session.refresh(postback)
            return postback
    
    async def get_postback(self, postback_id: int) -> Optional[Postback]:
        """Получить постбек по ID."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Postback).where(Postback.id == postback_id)
            )
            return result.scalars().first()
    
    # ===== Event методы =====
    
    async def create_event(self, user_id: int, event_type: str, data: Optional[str] = None) -> Event:
        """Создать событие."""
        async with self.async_session() as session:
            event = Event(user_id=user_id, event_type=event_type, data=data)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event
    
    # ===== Subscription методы =====
    
    async def get_subscription(self, user_id: int) -> Optional[Subscription]:
        """Получить подписку пользователя."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
            return result.scalars().first()
    
    async def create_subscription(self, user_id: int, plan: str, 
                                 expires_at: Optional[datetime] = None) -> Subscription:
        """Создать подписку."""
        async with self.async_session() as session:
            subscription = Subscription(
                user_id=user_id,
                plan=plan,
                expires_at=expires_at
            )
            session.add(subscription)
            await session.commit()
            await session.refresh(subscription)
            return subscription
    
    async def update_subscription(self, user_id: int, plan: str, 
                                 expires_at: Optional[datetime] = None) -> Optional[Subscription]:
        """Обновить подписку."""
        async with self.async_session() as session:
            result = await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
            subscription = result.scalars().first()
            if subscription:
                subscription.plan = plan
                if expires_at:
                    subscription.expires_at = expires_at
                subscription.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(subscription)
            return subscription


# Глобальный экземпляр БД
db = Database()
