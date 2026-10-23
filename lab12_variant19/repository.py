"""Repository на SQLAlchemy ORM."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from models import Instrument, Order, Trader


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self._s = session

    def create(
        self,
        trader_id: int,
        instrument_id: int,
        side: str,
        price: float,
        quantity: int,
    ) -> Order:
        order = Order(
            trader_id=trader_id,
            instrument_id=instrument_id,
            side=side.lower(),
            price=price,
            quantity=quantity,
        )
        self._s.add(order)
        self._s.commit()
        self._s.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(joinedload(Order.trader), joinedload(Order.instrument))
            .where(Order.id == order_id)
        )
        return self._s.scalars(stmt).first()

    def list_all(
        self,
        status: str | None = None,
        ticker: str | None = None,
        order_by_price: bool = False,
        desc: bool = False,
    ) -> List[Order]:
        stmt = select(Order).options(
            joinedload(Order.trader), joinedload(Order.instrument)
        )
        if status:
            stmt = stmt.where(Order.status == status)
        if ticker:
            stmt = stmt.join(Order.instrument).where(
                Instrument.ticker == ticker.upper()
            )
        if order_by_price:
            stmt = stmt.order_by(Order.price.desc() if desc else Order.price)
        else:
            stmt = stmt.order_by(Order.id)
        return list(self._s.scalars(stmt).unique().all())

    def update_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.get_by_id(order_id)
        if order is None:
            return None
        order.status = status
        self._s.commit()
        self._s.refresh(order)
        return order

    def delete(self, order_id: int) -> bool:
        order = self._s.get(Order, order_id)
        if order is None:
            return False
        self._s.delete(order)
        self._s.commit()
        return True

    def active_volume(self) -> float:
        stmt = select(func.coalesce(func.sum(Order.price * Order.quantity), 0.0)).where(
            Order.status == "active"
        )
        return float(self._s.scalar(stmt) or 0)

    def orders_of_trader(self, trader_id: int) -> List[Order]:
        stmt = (
            select(Order)
            .options(joinedload(Order.instrument))
            .where(Order.trader_id == trader_id)
        )
        return list(self._s.scalars(stmt).unique().all())

    def transfer_active(self, from_trader: int, to_trader: int) -> int:
        stmt = select(Order).where(
            Order.trader_id == from_trader, Order.status == "active"
        )
        orders = list(self._s.scalars(stmt).all())
        for o in orders:
            o.trader_id = to_trader
        self._s.commit()
        return len(orders)
