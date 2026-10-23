"""Сервисный слой с кэшированием."""

from __future__ import annotations

from typing import List, Optional

from cache import create_cache
from repository import OrderRepository


class OrderService:
    def __init__(self) -> None:
        self._repo = OrderRepository()
        self._cache = create_cache()

    def create_order(
        self, trader_id: int, instrument_id: int,
        side: str, price: float, quantity: int,
    ) -> dict:
        order = self._repo.create(trader_id, instrument_id, side, price, quantity)
        self._cache.delete("orders:all")
        self._cache.delete("orders:stats")
        return order

    def get_order(self, order_id: int) -> Optional[dict]:
        key = f"order:{order_id}"
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        order = self._repo.get_by_id(order_id)
        if order:
            self._cache.set(key, order, ttl=30)
        return order

    def list_orders(self, status: str | None = None, ticker: str | None = None) -> List[dict]:
        if status is None and ticker is None:
            cached = self._cache.get("orders:all")
            if cached is not None:
                return cached
            data = self._repo.list_all()
            self._cache.set("orders:all", data, ttl=15)
            return data
        return self._repo.list_all(status=status, ticker=ticker)

    def update_status(self, order_id: int, status: str) -> dict:
        if status not in ("active", "filled", "cancelled"):
            raise ValueError("status: active | filled | cancelled")
        order = self._repo.update_status(order_id, status)
        if order is None:
            raise KeyError(f"Заявка id={order_id} не найдена")
        self._cache.delete(f"order:{order_id}")
        self._cache.delete("orders:all")
        self._cache.delete("orders:stats")
        return order

    def delete_order(self, order_id: int) -> None:
        if not self._repo.delete(order_id):
            raise KeyError(f"Заявка id={order_id} не найдена")
        self._cache.delete(f"order:{order_id}")
        self._cache.delete("orders:all")
        self._cache.delete("orders:stats")

    def active_volume(self) -> float:
        return self._repo.active_volume()

    def stats(self) -> List[dict]:
        cached = self._cache.get("orders:stats")
        if cached is not None:
            return cached
        data = self._repo.stats_by_ticker()
        self._cache.set("orders:stats", data, ttl=30)
        return data

    def transfer(self, from_trader: int, to_trader: int) -> int:
        n = self._repo.transfer_orders(from_trader, to_trader)
        self._cache.clear()
        return n
