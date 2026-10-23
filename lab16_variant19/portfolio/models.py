"""
ЛР16 — Django-модели (вариант 19: инвестиционный портфель).
В полном проекте: django-admin startproject + startapp portfolio.
Здесь — модели и слой логики, совместимые с Django ORM API.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class Investor:
    id: int
    name: str
    email: str

@dataclass
class Asset:
    id: int
    ticker: str
    name: str
    asset_type: str
    price: float

@dataclass
class Portfolio:
    id: int
    investor_id: int
    name: str
    assets: List[tuple] = field(default_factory=list)

@dataclass
class Transaction:
    id: int
    portfolio_id: int
    asset_id: int
    side: str
    quantity: float
    price: float

class PortfolioStore:
    def __init__(self):
        self.investors = [Investor(1, "Иванов", "ivanov@mail.ru")]
        self.assets = [
            Asset(1, "SBER", "Сбербанк", "stock", 280.5),
            Asset(2, "GAZP", "Газпром", "stock", 160.0),
        ]
        self.portfolios = [Portfolio(1, 1, "Основной", [(1, 100), (2, 50)])]
        self.transactions: List[Transaction] = []
        self._tid = 1

    def portfolio_value(self, pid: int) -> float:
        p = next(x for x in self.portfolios if x.id == pid)
        total = 0.0
        for aid, qty in p.assets:
            a = next(x for x in self.assets if x.id == aid)
            total += qty * a.price
        return total

    def buy(self, pid: int, asset_id: int, qty: float, price: float) -> Transaction:
        p = next(x for x in self.portfolios if x.id == pid)
        found = False
        new_assets = []
        for aid, q in p.assets:
            if aid == asset_id:
                new_assets.append((aid, q + qty))
                found = True
            else:
                new_assets.append((aid, q))
        if not found:
            new_assets.append((asset_id, qty))
        p.assets = new_assets
        t = Transaction(self._tid, pid, asset_id, "buy", qty, price)
        self._tid += 1
        self.transactions.append(t)
        return t
