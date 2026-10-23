"""Контекстный менеджер."""

from __future__ import annotations

import time
from typing import Any, Optional


class OperationTimer:
    """Контекстный менеджер: измеряет время блока и пишет в лог."""

    def __init__(self, operation_name: str) -> None:
        self.operation_name = operation_name
        self.start: Optional[float] = None
        self.elapsed: float = 0.0

    def __enter__(self) -> OperationTimer:
        print(f"[CTX] Начало: {self.operation_name}")
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        if self.start is not None:
            self.elapsed = time.perf_counter() - self.start
        if exc_type is not None:
            print(
                f"[CTX] Ошибка в «{self.operation_name}»: {exc_val} "
                f"({self.elapsed:.4f} sec)"
            )
        else:
            print(
                f"[CTX] Завершено: {self.operation_name} "
                f"({self.elapsed:.4f} sec)"
            )
        return False
