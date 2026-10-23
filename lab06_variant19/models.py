"""Модели предметной области: биржевой портфель."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OperationStatus(Enum):
    CREATED = "создана"
    EXECUTED = "исполнена"
    CANCELLED = "отменена"


class InstrumentType(Enum):
    STOCK = "акция"
    BOND = "облигация"


@dataclass
class Instrument:
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

    def profit_estimate(self) -> float:
        return self.value * self.dividend_yield / 100


@dataclass
class Bond(Instrument):
    coupon_rate: float = 0.0
    nominal: float = 1000.0

    def profit_estimate(self) -> float:
        return self.quantity * self.nominal * self.coupon_rate / 100


@dataclass
class Operation:
    id: int
    instrument_id: int
    ticker: str
    operation_type: str
    quantity: int
    price: float
    status: OperationStatus = OperationStatus.CREATED

    @property
    def amount(self) -> float:
        return self.quantity * self.price
