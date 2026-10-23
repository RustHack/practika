"""Сервис портфеля."""

from __future__ import annotations

from typing import List

from factory import InstrumentFactory
from models import Instrument
from observers import Subject
from strategies import CalculationStrategy, RiskStrategy, ValueStrategy, YieldStrategy


class PortfolioService(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._instruments: List[Instrument] = []
        self._strategy: CalculationStrategy = ValueStrategy()

    def set_strategy(self, strategy: CalculationStrategy) -> None:
        self._strategy = strategy
        self.notify(f"Стратегия изменена на {type(strategy).__name__}")

    def add_instrument(self, instrument_type: str, **kwargs) -> Instrument:
        instr = InstrumentFactory.create(instrument_type, **kwargs)
        self._instruments.append(instr)
        self.notify(f"Добавлен инструмент {instr.ticker} ({instrument_type})")
        return instr

    def get_all(self) -> List[Instrument]:
        return list(self._instruments)

    def calculate(self) -> float:
        result = self._strategy.calculate(self._instruments)
        self.notify(f"Расчёт выполнен: {result:,.2f}")
        return result

    def portfolio_value(self) -> float:
        self.set_strategy(ValueStrategy())
        return self.calculate()

    def portfolio_yield(self) -> float:
        self.set_strategy(YieldStrategy())
        return self.calculate()

    def portfolio_risk(self) -> float:
        self.set_strategy(RiskStrategy())
        return self.calculate()
