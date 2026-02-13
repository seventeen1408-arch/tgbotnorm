"""
Модели базы данных.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), nullable=True)
    is_vip = Column(Boolean, default=False)
    signals_unlocked_until = Column(DateTime, nullable=True)
    last_free_signal = Column(DateTime, nullable=True)
    deposit_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Signal(Base):
    """Модель сигнала."""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True)
    game_name = Column(String(255))
    coefficient = Column(Float)
    time_utc = Column(String(10))
    is_vip_only = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Postback(Base):
    """Модель постбека от казино."""
    __tablename__ = "postbacks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    casino_id = Column(String(50))
    event_type = Column(String(50))  # deposit, withdrawal, bet, win
    amount = Column(Float)
    status = Column(String(20))  # pending, confirmed, rejected
    raw_data = Column(Text)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    """Модель события пользователя."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    event_type = Column(String(50))  # signal_view, button_click, vip_purchase
    data = Column(Text, nullable=True)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    """Модель подписки."""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    plan = Column(String(50))  # free, vip
    expires_at = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
