"""Протоколы."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Valuable(Protocol):
    """Протокол: объект, имеющий стоимость."""

    @property
    def value(self) -> float:
        ...

    def profit_estimate(self) -> float:
        ...
