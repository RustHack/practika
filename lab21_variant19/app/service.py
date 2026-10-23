from __future__ import annotations
from app.models import Asset, Portfolio, Trade, User

class TradingSystem:
    def __init__(self) -> None:
        self.users = {1: User(1, "Иванов")}
        self.assets = {
            "SBER": Asset(1, "SBER", 280.5),
            "GAZP": Asset(2, "GAZP", 160.0),
        }
        self.portfolios = {1: Portfolio(1)}
        self.trades: list[Trade] = []
        self._tid = 1

    def buy(self, user_id: int, ticker: str, qty: float) -> Trade:
        p = self.portfolios[user_id]
        asset = self.assets[ticker]
        cost = asset.price * qty
        if cost > p.cash:
            raise ValueError("Недостаточно средств")
        p.cash -= cost
        p.positions[ticker] = p.positions.get(ticker, 0) + qty
        t = Trade(self._tid, user_id, ticker, "buy", qty, asset.price)
        self._tid += 1
        self.trades.append(t)
        return t

    def sell(self, user_id: int, ticker: str, qty: float) -> Trade:
        p = self.portfolios[user_id]
        if p.positions.get(ticker, 0) < qty:
            raise ValueError("Недостаточно бумаг")
        asset = self.assets[ticker]
        p.positions[ticker] -= qty
        p.cash += asset.price * qty
        t = Trade(self._tid, user_id, ticker, "sell", qty, asset.price)
        self._tid += 1
        self.trades.append(t)
        return t

    def value(self, user_id: int) -> float:
        p = self.portfolios[user_id]
        total = p.cash
        for t, q in p.positions.items():
            total += q * self.assets[t].price
        return total
