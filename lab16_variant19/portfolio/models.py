"""
ЛР16 — Django-модели (вариант 19: инвестиционный портфель).
В полном проекте: django-admin startproject + startapp portfolio.
Здесь — модели и слой логики, совместимые с Django ORM API.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


# --- Имитация Django models (без реального Django, чтобы lab запускалась без установки) ---

@dataclass
class Instrument:
    """Модель инструмента (аналог models.Model)."""
    ticker: str
    name: str
    asset_class: str  # stock, bond, etf, crypto
    last_price: float = 0.0
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.ticker} — {self.name}"


@dataclass
class Portfolio:
    name: str
    owner: str
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"Portfolio({self.name})"


@dataclass
class Position:
    portfolio: Portfolio
    instrument: Instrument
    quantity: float
    avg_price: float
    id: Optional[int] = None

    @property
    def market_value(self) -> float:
        return self.quantity * self.instrument.last_price

    @property
    def pnl(self) -> float:
        return self.market_value - self.quantity * self.avg_price

    def __str__(self) -> str:
        return f"{self.instrument.ticker}: {self.quantity} @ {self.avg_price}"


# Простой in-memory «ORM» для демонстрации
class _Manager:
    def __init__(self, model_cls):
        self._model = model_cls
        self._items: List = []
        self._pk = 1

    def create(self, **kwargs):
        obj = self._model(**kwargs)
        obj.id = self._pk
        self._pk += 1
        self._items.append(obj)
        return obj

    def all(self):
        return list(self._items)

    def filter(self, **kwargs):
        result = self._items
        for k, v in kwargs.items():
            result = [x for x in result if getattr(x, k, None) == v]
        return result

    def get(self, **kwargs):
        found = self.filter(**kwargs)
        if not found:
            raise ValueError("DoesNotExist")
        return found[0]


# Подвешиваем managers как в Django
Instrument.objects = _Manager(Instrument)  # type: ignore
Portfolio.objects = _Manager(Portfolio)  # type: ignore
Position.objects = _Manager(Position)  # type: ignore
