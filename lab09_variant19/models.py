"""Бизнес-логика: биржевые заявки (вариант 19)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Order:
    id: int
    ticker: str
    side: str
    price: float
    quantity: int
    status: str = "active"

    @property
    def amount(self) -> float:
        return self.price * self.quantity


class OrderService:
    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._next_id = 1
        self.create_order("SBER", "buy", 280.5, 100)
        self.create_order("GAZP", "sell", 160.0, 50)
        self.create_order("SBER", "sell", 285.0, 30)

    def create_order(self, ticker: str, side: str, price: float, quantity: int) -> Order:
        side = side.lower().strip()
        if side not in ("buy", "sell"):
            raise ValueError("side должен быть buy или sell")
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if not ticker.strip():
            raise ValueError("Тикер не может быть пустым")

        order = Order(
            id=self._next_id,
            ticker=ticker.upper().strip(),
            side=side,
            price=float(price),
            quantity=int(quantity),
            status="active",
        )
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._orders.get(order_id)

    def list_orders(self) -> List[Order]:
        return list(self._orders.values())

    def list_active(self) -> List[Order]:
        return [o for o in self._orders.values() if o.status == "active"]

    def cancel_order(self, order_id: int) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Заявка id={order_id} не найдена")
        if order.status != "active":
            raise ValueError(f"Заявка уже в статусе «{order.status}»")
        order.status = "cancelled"
        return order

    def fill_order(self, order_id: int) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Заявка id={order_id} не найдена")
        if order.status != "active":
            raise ValueError(f"Заявка уже в статусе «{order.status}»")
        order.status = "filled"
        return order

    def portfolio_value(self) -> float:
        return sum(o.amount for o in self.list_active())

    def filter_by_ticker(self, ticker: str) -> List[Order]:
        t = ticker.upper().strip()
        return [o for o in self._orders.values() if o.ticker == t]
