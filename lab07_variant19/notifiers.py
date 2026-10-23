"""Реализации уведомлений (OCP, DIP)."""

from __future__ import annotations

from interfaces import Notifier


class ConsoleNotifier(Notifier):
    def notify(self, message: str) -> None:
        print(f"[NOTIFY] {message}")


class SilentNotifier(Notifier):
    """Для тестов / без вывода."""
    def notify(self, message: str) -> None:
        pass
