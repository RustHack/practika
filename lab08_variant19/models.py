"""Модели инструментов."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


@dataclass
class Instrument(ABC):
    id: int
    ticker: str
    name: str
    price: float
    quantity: int = 0

    @property
    def value(self) -> float:
        return self.price * self.quantity


@dataclass
class Stock(Instrument):
    dividend_yield: float = 0.0


@dataclass
class Bond(Instrument):
    coupon_rate: float = 0.0
    nominal: float = 1000.0


@dataclass
class Fund(Instrument):
    management_fee: float = 1.0
