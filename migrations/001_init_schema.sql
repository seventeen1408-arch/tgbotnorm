-- Инициализация схемы базы данных

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    is_vip BOOLEAN DEFAULT FALSE,
    signals_unlocked_until TIMESTAMP,
    last_free_signal TIMESTAMP,
    deposit_amount FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_users_is_vip ON users(is_vip);

-- Таблица сигналов
CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    game_name VARCHAR(255) NOT NULL,
    coefficient FLOAT NOT NULL,
    time_utc VARCHAR(10) NOT NULL,
    is_vip_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_signals_game_name ON signals(game_name);
CREATE INDEX idx_signals_is_vip_only ON signals(is_vip_only);

-- Таблица постбеков от казино
CREATE TABLE IF NOT EXISTS postbacks (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    casino_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_postbacks_user_id ON postbacks(user_id);
CREATE INDEX idx_postbacks_casino_id ON postbacks(casino_id);
CREATE INDEX idx_postbacks_status ON postbacks(status);

-- Таблица событий пользователя
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_event_type ON events(event_type);

-- Таблица подписок
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    plan VARCHAR(50) NOT NULL,
    expires_at TIMESTAMP,
    auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_plan ON subscriptions(plan);

-- Таблица платежей
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(10),
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    external_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_external_id ON payments(external_id);
