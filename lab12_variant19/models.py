"""ORM-модели SQLAlchemy 2.x — биржевые заявки (вариант 19)."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, Float, Integer, DateTime, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Trader(Base):
    __tablename__ = "traders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    orders: Mapped[List["Order"]] = relationship(back_populates="trader")

    def __repr__(self) -> str:
        return f"Trader(id={self.id}, name={self.name!r})"


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    instrument_type: Mapped[str] = mapped_column(String(20), nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="instrument")

    def __repr__(self) -> str:
        return f"Instrument(id={self.id}, ticker={self.ticker!r})"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("side IN ('buy', 'sell')", name="ck_side"),
        CheckConstraint("status IN ('active', 'filled', 'cancelled')", name="ck_status"),
        CheckConstraint("price > 0", name="ck_price"),
        CheckConstraint("quantity > 0", name="ck_qty"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    trader_id: Mapped[int] = mapped_column(ForeignKey("traders.id"), nullable=False)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), nullable=False)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    trader: Mapped["Trader"] = relationship(back_populates="orders")
    instrument: Mapped["Instrument"] = relationship(back_populates="orders")

    @property
    def amount(self) -> float:
        return self.price * self.quantity

    def __repr__(self) -> str:
        return f"Order(id={self.id}, {self.side} {self.quantity}@{self.price})"
