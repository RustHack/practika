"""Подключение к SQLite и инициализация схемы."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path("/tmp/lab11_trading.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS traders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS instruments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker      TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    instrument_type TEXT NOT NULL CHECK(instrument_type IN ('stock','bond','fund')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    trader_id       INTEGER NOT NULL,
    instrument_id   INTEGER NOT NULL,
    side            TEXT NOT NULL CHECK(side IN ('buy','sell')),
    price           REAL NOT NULL CHECK(price > 0),
    quantity        INTEGER NOT NULL CHECK(quantity > 0),
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK(status IN ('active','filled','cancelled')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (trader_id) REFERENCES traders(id),
    FOREIGN KEY (instrument_id) REFERENCES instruments(id)
);

CREATE TABLE IF NOT EXISTS order_tags (
    order_id    INTEGER NOT NULL,
    tag         TEXT NOT NULL,
    PRIMARY KEY (order_id, tag),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_orders_trader ON orders(trader_id);
CREATE INDEX IF NOT EXISTS idx_orders_instrument ON orders(instrument_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_instruments_ticker ON instruments(ticker);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        n = conn.execute("SELECT COUNT(*) FROM traders").fetchone()[0]
        if n == 0:
            conn.execute(
                "INSERT INTO traders(name, email) VALUES (?, ?), (?, ?)",
                ("Иванов И.И.", "ivanov@mail.ru", "Петрова А.С.", "petrova@mail.ru"),
            )
            conn.execute(
                """INSERT INTO instruments(ticker, name, instrument_type) VALUES
                   ('SBER', 'Сбербанк', 'stock'),
                   ('GAZP', 'Газпром', 'stock'),
                   ('OFZ26238', 'ОФЗ 26238', 'bond'),
                   ('FXUS', 'FinEx USA', 'fund')"""
            )
            conn.execute(
                """INSERT INTO orders(trader_id, instrument_id, side, price, quantity, status)
                   VALUES
                   (1, 1, 'buy', 280.5, 100, 'active'),
                   (1, 2, 'sell', 160.0, 50, 'active'),
                   (2, 1, 'buy', 275.0, 200, 'filled'),
                   (2, 3, 'buy', 980.0, 10, 'active'),
                   (1, 4, 'buy', 5500.0, 5, 'cancelled'),
                   (2, 2, 'sell', 165.0, 30, 'active'),
                   (1, 1, 'sell', 290.0, 40, 'active'),
                   (2, 4, 'buy', 5400.0, 3, 'active'),
                   (1, 3, 'buy', 975.0, 15, 'filled'),
                   (2, 1, 'sell', 282.0, 80, 'active')"""
            )
            conn.execute(
                """INSERT INTO order_tags(order_id, tag) VALUES
                   (1, 'priority'), (1, 'sber'),
                   (3, 'filled'), (4, 'bond'),
                   (7, 'sber')"""
            )
            conn.commit()
