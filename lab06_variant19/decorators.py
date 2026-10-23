"""Декораторы."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def log_call(func: F) -> F:
    """Декоратор №1 — журналирование вызова."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] вызван {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__}() завершён")
        return result
    return wrapper  # type: ignore


def measure_time(func: F) -> F:
    """Декоратор №2 — измерение времени выполнения."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[PERFORMANCE] {func.__name__}: {elapsed:.4f} sec")
        return result
    return wrapper  # type: ignore


def limit_calls(max_calls: int) -> Callable[[F], F]:
    """Декоратор №3 — с параметром. Ограничивает число вызовов."""
    def decorator(func: F) -> F:
        calls = {"count": 0}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if calls["count"] >= max_calls:
                raise RuntimeError(
                    f"Превышен лимит вызовов {func.__name__}() "
                    f"({max_calls})"
                )
            calls["count"] += 1
            return func(*args, **kwargs)

        return wrapper  # type: ignore
    return decorator
