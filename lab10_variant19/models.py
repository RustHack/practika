"""Модели и хранилище биржевых заявок."""

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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ticker": self.ticker,
            "side": self.side,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "amount": self.amount,
        }


class OrderRepository:
    def __init__(self) -> None:
        self._items: Dict[int, Order] = {}
        self._next_id = 1

    def add(self, ticker: str, side: str, price: float, quantity: int) -> Order:
        order = Order(self._next_id, ticker.upper(), side.lower(), price, quantity)
        self._items[order.id] = order
        self._next_id += 1
        return order

    def get(self, order_id: int) -> Optional[Order]:
        return self._items.get(order_id)

    def get_all(self) -> List[Order]:
        return list(self._items.values())

    def delete(self, order_id: int) -> bool:
        if order_id in self._items:
            del self._items[order_id]
            return True
        return False

    def update(self, order: Order) -> None:
        self._items[order.id] = order


class OrderService:
    def __init__(self, repo: OrderRepository | None = None) -> None:
        self._repo = repo or OrderRepository()
        self.create("SBER", "buy", 280.5, 100)
        self.create("GAZP", "sell", 160.0, 50)
        self.create("SBER", "sell", 285.0, 30)

    def create(self, ticker: str, side: str, price: float, quantity: int) -> Order:
        side = side.lower().strip()
        if side not in ("buy", "sell"):
            raise ValueError("side должен быть buy или sell")
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if not ticker.strip():
            raise ValueError("Тикер не может быть пустым")
        return self._repo.add(ticker.strip(), side, float(price), int(quantity))

    def get(self, order_id: int) -> Order:
        order = self._repo.get(order_id)
        if order is None:
            raise KeyError(f"Заявка id={order_id} не найдена")
        return order

    def list(self, ticker: str | None = None, side: str | None = None,
             status: str | None = None) -> List[Order]:
        result = self._repo.get_all()
        if ticker:
            result = [o for o in result if o.ticker == ticker.upper()]
        if side:
            result = [o for o in result if o.side == side.lower()]
        if status:
            result = [o for o in result if o.status == status.lower()]
        return result

    def update(self, order_id: int, **fields) -> Order:
        order = self.get(order_id)
        if "ticker" in fields:
            order.ticker = str(fields["ticker"]).upper()
        if "side" in fields:
            s = str(fields["side"]).lower()
            if s not in ("buy", "sell"):
                raise ValueError("side должен быть buy или sell")
            order.side = s
        if "price" in fields:
            p = float(fields["price"])
            if p <= 0:
                raise ValueError("Цена должна быть положительной")
            order.price = p
        if "quantity" in fields:
            q = int(fields["quantity"])
            if q <= 0:
                raise ValueError("Количество должно быть положительным")
            order.quantity = q
        if "status" in fields:
            st = str(fields["status"]).lower()
            if st not in ("active", "filled", "cancelled"):
                raise ValueError("status: active | filled | cancelled")
            order.status = st
        self._repo.update(order)
        return order

    def delete(self, order_id: int) -> None:
        if not self._repo.delete(order_id):
            raise KeyError(f"Заявка id={order_id} не найдена")

    def list_active(self) -> List[Order]:
        return [o for o in self._repo.get_all() if o.status == "active"]

    def active_volume(self) -> float:
        return sum(o.amount for o in self.list_active())
