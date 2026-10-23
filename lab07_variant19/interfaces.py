"""Интерфейсы и протоколы (ISP, DIP)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, runtime_checkable

from models import FinancialInstrument


@runtime_checkable
class ProfitCalculator(Protocol):
    """Интерфейс расчёта прибыли (ISP)."""
    def calculate_profit(self) -> float: ...


class InstrumentRepository(ABC):
    """Абстракция хранилища (DIP)."""

    @abstractmethod
    def add(self, instrument: FinancialInstrument) -> None: ...

    @abstractmethod
    def get_by_id(self, instrument_id: int) -> Optional[FinancialInstrument]: ...

    @abstractmethod
    def get_all(self) -> List[FinancialInstrument]: ...

    @abstractmethod
    def update(self, instrument: FinancialInstrument) -> None: ...


class Notifier(ABC):
    """Абстракция уведомлений (DIP + ISP)."""

    @abstractmethod
    def notify(self, message: str) -> None: ...
