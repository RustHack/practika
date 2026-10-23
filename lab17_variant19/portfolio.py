"""Учебная модель портфеля для Telegram-бота."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Position:
    ticker: str
    quantity: float
    avg_price: float

@dataclass
class Portfolio:
    cash: float = 100_000.0
    positions: Dict[str, Position] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)

    def value(self, prices: Dict[str, float]) -> float:
        total = self.cash
        for t, p in self.positions.items():
            total += p.quantity * prices.get(t, p.avg_price)
        return total

    def buy(self, ticker: str, qty: float, price: float) -> str:
        cost = qty * price
        if cost > self.cash:
            return "Недостаточно средств"
        self.cash -= cost
        if ticker in self.positions:
            pos = self.positions[ticker]
            new_qty = pos.quantity + qty
            pos.avg_price = (pos.avg_price * pos.quantity + price * qty) / new_qty
            pos.quantity = new_qty
        else:
            self.positions[ticker] = Position(ticker, qty, price)
        msg = f"BUY {qty} {ticker} @ {price}"
        self.history.append(msg)
        return msg

    def sell(self, ticker: str, qty: float, price: float) -> str:
        if ticker not in self.positions or self.positions[ticker].quantity < qty:
            return "Недостаточно бумаг"
        self.positions[ticker].quantity -= qty
        self.cash += qty * price
        if self.positions[ticker].quantity == 0:
            del self.positions[ticker]
        msg = f"SELL {qty} {ticker} @ {price}"
        self.history.append(msg)
        return msg

PRICES = {"SBER": 280.5, "GAZP": 160.0, "FXUS": 5500.0}
