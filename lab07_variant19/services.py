"""Сервисный слой (SRP, DIP)."""

from __future__ import annotations

from typing import List, Optional

from interfaces import InstrumentRepository, Notifier, ProfitCalculator
from models import Bond, FinancialInstrument, Fund, Stock


class PortfolioService:
    def __init__(
        self,
        repository: InstrumentRepository,
        notifier: Notifier,
    ) -> None:
        self._repo = repository
        self._notifier = notifier
        self._next_id = 1

    def add_stock(
        self,
        ticker: str,
        name: str,
        price: float,
        quantity: int = 0,
        dividend_yield: float = 0.0,
    ) -> Stock:
        stock = Stock(
            id=self._next_id,
            ticker=ticker.upper(),
            name=name,
            price=price,
            quantity=quantity,
            dividend_yield=dividend_yield,
        )
        self._repo.add(stock)
        self._next_id += 1
        self._notifier.notify(f"Добавлена акция {stock.ticker}")
        return stock

    def add_bond(
        self,
        ticker: str,
        name: str,
        price: float,
        quantity: int = 0,
        coupon_rate: float = 0.0,
        nominal: float = 1000.0,
    ) -> Bond:
        bond = Bond(
            id=self._next_id,
            ticker=ticker.upper(),
            name=name,
            price=price,
            quantity=quantity,
            coupon_rate=coupon_rate,
            nominal=nominal,
        )
        self._repo.add(bond)
        self._next_id += 1
        self._notifier.notify(f"Добавлена облигация {bond.ticker}")
        return bond

    def add_fund(
        self,
        ticker: str,
        name: str,
        price: float,
        quantity: int = 0,
        management_fee: float = 1.0,
    ) -> Fund:
        fund = Fund(
            id=self._next_id,
            ticker=ticker.upper(),
            name=name,
            price=price,
            quantity=quantity,
            management_fee=management_fee,
        )
        self._repo.add(fund)
        self._next_id += 1
        self._notifier.notify(f"Добавлен фонд {fund.ticker}")
        return fund

    def buy(self, instrument_id: int, quantity: int, price: float) -> None:
        instr = self._repo.get_by_id(instrument_id)
        if instr is None:
            raise ValueError(f"Инструмент id={instrument_id} не найден")
        instr.quantity += quantity
        instr.price = price
        self._repo.update(instr)
        self._notifier.notify(f"Покупка {quantity} шт. {instr.ticker}")

    def sell(self, instrument_id: int, quantity: int) -> None:
        instr = self._repo.get_by_id(instrument_id)
        if instr is None:
            raise ValueError(f"Инструмент id={instrument_id} не найден")
        if instr.quantity < quantity:
            raise ValueError("Недостаточно бумаг")
        instr.quantity -= quantity
        self._repo.update(instr)
        self._notifier.notify(f"Продажа {quantity} шт. {instr.ticker}")

    def portfolio_value(self) -> float:
        return sum(i.value for i in self._repo.get_all())

    def total_profit(self) -> float:
        total = 0.0
        for item in self._repo.get_all():
            if isinstance(item, ProfitCalculator):
                total += item.calculate_profit()
        return total

    def get_all(self) -> List[FinancialInstrument]:
        return self._repo.get_all()

    def get_by_id(self, instrument_id: int) -> Optional[FinancialInstrument]:
        return self._repo.get_by_id(instrument_id)
