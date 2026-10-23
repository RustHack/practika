"""Реализации хранилища (DIP)."""

from __future__ import annotations

from typing import List, Optional

from interfaces import InstrumentRepository
from models import FinancialInstrument


class InMemoryInstrumentRepository(InstrumentRepository):
    """Хранилище в памяти."""

    def __init__(self) -> None:
        self._items: List[FinancialInstrument] = []

    def add(self, instrument: FinancialInstrument) -> None:
        self._items.append(instrument)

    def get_by_id(self, instrument_id: int) -> Optional[FinancialInstrument]:
        for item in self._items:
            if item.id == instrument_id:
                return item
        return None

    def get_all(self) -> List[FinancialInstrument]:
        return list(self._items)

    def update(self, instrument: FinancialInstrument) -> None:
        for i, item in enumerate(self._items):
            if item.id == instrument.id:
                self._items[i] = instrument
                return
