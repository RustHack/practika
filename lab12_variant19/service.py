"""Сервисный слой."""

from __future__ import annotations

from typing import List

from database import get_session
from models import Order
from repository import OrderRepository


class OrderService:
    def create(
        self, trader_id: int, instrument_id: int, side: str, price: float, quantity: int
    ) -> Order:
        if side.lower() not in ("buy", "sell"):
            raise ValueError("side: buy | sell")
        if price <= 0 or quantity <= 0:
            raise ValueError("price и quantity должны быть > 0")
        with get_session() as session:
            repo = OrderRepository(session)
            return repo.create(trader_id, instrument_id, side, price, quantity)

    def get(self, order_id: int) -> Order:
        with get_session() as session:
            repo = OrderRepository(session)
            order = repo.get_by_id(order_id)
            if order is None:
                raise KeyError(f"Заявка {order_id} не найдена")
            _ = order.trader.name, order.instrument.ticker
            session.expunge(order)
            return order

    def list(
        self,
        status: str | None = None,
        ticker: str | None = None,
        sort_price: bool = False,
        desc: bool = False,
    ) -> List[Order]:
        with get_session() as session:
            repo = OrderRepository(session)
            orders = repo.list_all(status, ticker, sort_price, desc)
            for o in orders:
                _ = o.trader.name, o.instrument.ticker
                session.expunge(o)
            return orders

    def set_status(self, order_id: int, status: str) -> Order:
        if status not in ("active", "filled", "cancelled"):
            raise ValueError("status: active | filled | cancelled")
        with get_session() as session:
            repo = OrderRepository(session)
            order = repo.update_status(order_id, status)
            if order is None:
                raise KeyError(f"Заявка {order_id} не найдена")
            _ = order.trader.name, order.instrument.ticker
            session.expunge(order)
            return order

    def delete(self, order_id: int) -> None:
        with get_session() as session:
            repo = OrderRepository(session)
            if not repo.delete(order_id):
                raise KeyError(f"Заявка {order_id} не найдена")

    def active_volume(self) -> float:
        with get_session() as session:
            return OrderRepository(session).active_volume()

    def trader_orders(self, trader_id: int) -> List[Order]:
        with get_session() as session:
            repo = OrderRepository(session)
            orders = repo.orders_of_trader(trader_id)
            for o in orders:
                _ = o.instrument.ticker
                session.expunge(o)
            return orders

    def transfer(self, from_trader: int, to_trader: int) -> int:
        with get_session() as session:
            return OrderRepository(session).transfer_active(from_trader, to_trader)
