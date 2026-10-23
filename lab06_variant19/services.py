"""
Сервисы портфеля и ордеров для лабораторной 6.
"""
from __future__ import annotations

from typing import Dict, List, Optional
from copy import deepcopy

from models import Instrument, Position, Order, OrderSide, OrderStatus


class PortfolioService:
    """Управление инструментами и позициями."""

    def __init__(self) -> None:
        self._instruments: Dict[str, Instrument] = {}
        self._positions: Dict[str, Position] = {}
        self._snapshot: Optional[dict] = None

    # --- инструменты ---

    def add_instrument(self, instrument: Instrument) -> None:
        self._instruments[instrument.ticker] = instrument

    def get_instrument(self, ticker: str) -> Optional[Instrument]:
        return self._instruments.get(ticker)

    def get_price(self, ticker: str) -> float:
        inst = self._instruments.get(ticker)
        if inst is None:
            raise KeyError(f"Инструмент {ticker} не найден")
        return inst.price

    def update_price(self, ticker: str, price: float) -> None:
        inst = self._instruments.get(ticker)
        if inst is None:
            raise KeyError(f"Инструмент {ticker} не найден")
        inst.price = price
        if ticker in self._positions:
            self._positions[ticker].current_price = price

    # --- позиции ---

    def open_position(self, ticker: str, quantity: float, avg_price: float) -> Position:
        inst = self._instruments.get(ticker)
        if inst is None:
            raise KeyError(f"Инструмент {ticker} не найден")
        if ticker in self._positions:
            pos = self._positions[ticker]
            total_qty = pos.quantity + quantity
            pos.avg_price = (pos.avg_price * pos.quantity + avg_price * quantity) / total_qty
            pos.quantity = total_qty
            pos.current_price = inst.price
            return pos
        pos = Position(
            instrument=inst,
            quantity=quantity,
            avg_price=avg_price,
            current_price=inst.price,
        )
        self._positions[ticker] = pos
        return pos

    def close_position(self, ticker: str, quantity: Optional[float] = None) -> None:
        if ticker not in self._positions:
            raise KeyError(f"Позиция {ticker} не найдена")
        pos = self._positions[ticker]
        if quantity is None or quantity >= pos.quantity:
            del self._positions[ticker]
        else:
            pos.quantity -= quantity

    @property
    def positions(self) -> List[Position]:
        return list(self._positions.values())

    def total_value(self) -> float:
        return sum(p.market_value for p in self._positions.values())

    def total_pnl(self) -> float:
        return sum(p.pnl for p in self._positions.values())

    # --- snapshot для транзакций ---

    def save_snapshot(self) -> None:
        self._snapshot = {
            "instruments": deepcopy(self._instruments),
            "positions": deepcopy(self._positions),
        }

    def restore_snapshot(self) -> None:
        if self._snapshot is None:
            return
        self._instruments = self._snapshot["instruments"]
        self._positions = self._snapshot["positions"]
        self._snapshot = None

    def clear_snapshot(self) -> None:
        self._snapshot = None


class OrderService:
    """Размещение и исполнение ордеров."""

    def __init__(self, portfolio: PortfolioService) -> None:
        self._portfolio = portfolio
        self._orders: List[Order] = []
        self._next_id = 1

    def place_order(
        self,
        ticker: str,
        side: OrderSide,
        quantity: float,
        price: float,
    ) -> Order:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price <= 0:
            raise ValueError("price must be positive")
        if self._portfolio.get_instrument(ticker) is None:
            raise KeyError(f"Инструмент {ticker} не найден")

        order = Order(
            id=self._next_id,
            ticker=ticker,
            side=side,
            quantity=quantity,
            price=price,
            status=OrderStatus.NEW,
        )
        self._next_id += 1
        self._orders.append(order)
        self._execute(order)
        return order

    def _execute(self, order: Order) -> None:
        try:
            if order.side == OrderSide.BUY:
                self._portfolio.open_position(order.ticker, order.quantity, order.price)
            else:
                self._portfolio.close_position(order.ticker, order.quantity)
            order.status = OrderStatus.FILLED
        except Exception:
            order.status = OrderStatus.REJECTED
            raise

    @property
    def orders(self) -> List[Order]:
        return list(self._orders)
