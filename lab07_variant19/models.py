"""Модели: финансовые инструменты (S, L, O)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FinancialInstrument(ABC):
    """Базовый абстрактный инструмент (OCP + LSP)."""
    id: int
    ticker: str
    name: str
    price: float
    quantity: int = 0

    @property
    def value(self) -> float:
        return self.price * self.quantity

    @abstractmethod
    def calculate_profit(self) -> float:
        """Каждый тип считает прибыль по-своему (OCP)."""
        ...


@dataclass
class Stock(FinancialInstrument):
    """Акция."""
    dividend_yield: float = 0.0

    def calculate_profit(self) -> float:
        return self.value * self.dividend_yield / 100


@dataclass
class Bond(FinancialInstrument):
    """Облигация."""
    coupon_rate: float = 0.0
    nominal: float = 1000.0

    def calculate_profit(self) -> float:
        return self.quantity * self.nominal * self.coupon_rate / 100


@dataclass
class Fund(FinancialInstrument):
    """Фонд."""
    management_fee: float = 1.0

    def calculate_profit(self) -> float:
        return self.value * (5.0 - self.management_fee) / 100
