"""Паттерн Observer."""

from __future__ import annotations

from typing import List, Protocol


class Observer(Protocol):
    def update(self, event: str) -> None: ...


class ConsoleObserver:
    def update(self, event: str) -> None:
        print(f"[OBSERVER] {event}")


class LogObserver:
    def __init__(self) -> None:
        self.events: List[str] = []

    def update(self, event: str) -> None:
        self.events.append(event)
        print(f"[LOG] {event}")


class Subject:
    """Источник событий."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str) -> None:
        for obs in self._observers:
            obs.update(event)
