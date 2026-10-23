"""
Модели предметной области — инвестиционный портфель.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    NEW = "new"
    FILLED = "filled"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@dataclass
class Instrument:
    ticker: str
    name: str
    asset_class: str
    price: float

    def __str__(self) -> str:
        return f"{self.ticker} ({self.name}) @ {self.price}"


@dataclass
class Position:
    instrument: Instrument
    quantity: float
    avg_price: float
    current_price: float

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.avg_price

    @property
    def pnl(self) -> float:
        return self.market_value - self.cost_basis

    def __str__(self) -> str:
        return (
            f"{self.instrument.ticker}: qty={self.quantity} "
            f"avg={self.avg_price:.2f} cur={self.current_price:.2f} "
            f"PnL={self.pnl:+.2f}"
        )


@dataclass
class Order:
    id: int
    ticker: str
    side: OrderSide
    quantity: float
    price: float
    status: OrderStatus = OrderStatus.NEW
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return (
            f"Order#{self.id} {self.side.value} {self.quantity} {self.ticker} "
            f"@ {self.price} [{self.status.value}]"
        )
