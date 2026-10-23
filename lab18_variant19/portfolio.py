"""Биржевой симулятор для тестирования (ЛР18, вар.19)."""
from __future__ import annotations
from typing import Dict, Protocol

class QuoteProvider(Protocol):
    def get_price(self, ticker: str) -> float: ...

class StaticQuotes:
    def __init__(self, data: Dict[str, float]):
        self.data = data
    def get_price(self, ticker: str) -> float:
        if ticker not in self.data:
            raise KeyError(ticker)
        return self.data[ticker]

class Portfolio:
    def __init__(self, cash: float, quotes: QuoteProvider):
        self.cash = cash
        self.positions: Dict[str, float] = {}
        self.quotes = quotes

    def buy(self, ticker: str, qty: float) -> None:
        price = self.quotes.get_price(ticker)
        cost = price * qty
        if cost > self.cash:
            raise ValueError("Недостаточно средств")
        self.cash -= cost
        self.positions[ticker] = self.positions.get(ticker, 0) + qty

    def sell(self, ticker: str, qty: float) -> None:
        if self.positions.get(ticker, 0) < qty:
            raise ValueError("Недостаточно бумаг")
        price = self.quotes.get_price(ticker)
        self.positions[ticker] -= qty
        self.cash += price * qty

    def value(self) -> float:
        total = self.cash
        for t, q in self.positions.items():
            total += q * self.quotes.get_price(t)
        return total
