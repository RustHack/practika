"""Подключение к БД (SQLite для локальной работы)."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Instrument, Order, Trader

DB_PATH = Path("/tmp/lab12_trading.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        if session.scalar(select(Trader).limit(1)) is None:
            t1 = Trader(name="Иванов И.И.", email="ivanov@mail.ru")
            t2 = Trader(name="Петрова А.С.", email="petrova@mail.ru")
            session.add_all([t1, t2])
            session.flush()
            instruments = [
                Instrument(ticker="SBER", name="Сбербанк", instrument_type="stock"),
                Instrument(ticker="GAZP", name="Газпром", instrument_type="stock"),
                Instrument(ticker="OFZ26238", name="ОФЗ 26238", instrument_type="bond"),
                Instrument(ticker="FXUS", name="FinEx USA", instrument_type="fund"),
            ]
            session.add_all(instruments)
            session.flush()
            session.add_all([
                Order(trader_id=t1.id, instrument_id=1, side="buy", price=280.5, quantity=100),
                Order(trader_id=t1.id, instrument_id=2, side="sell", price=160.0, quantity=50),
                Order(trader_id=t2.id, instrument_id=1, side="buy", price=275.0, quantity=200, status="filled"),
                Order(trader_id=t2.id, instrument_id=3, side="buy", price=980.0, quantity=10),
                Order(trader_id=t1.id, instrument_id=4, side="buy", price=5500.0, quantity=5, status="cancelled"),
                Order(trader_id=t2.id, instrument_id=2, side="sell", price=165.0, quantity=30),
                Order(trader_id=t1.id, instrument_id=1, side="sell", price=290.0, quantity=40),
                Order(trader_id=t2.id, instrument_id=4, side="buy", price=5400.0, quantity=3),
                Order(trader_id=t1.id, instrument_id=3, side="buy", price=975.0, quantity=15, status="filled"),
                Order(trader_id=t2.id, instrument_id=1, side="sell", price=282.0, quantity=80),
            ])
            session.commit()


def get_session() -> Session:
    return SessionLocal()
