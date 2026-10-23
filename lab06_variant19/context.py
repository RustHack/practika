"""
Контекстные менеджеры для лабораторной 6.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Type, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


@contextmanager
def portfolio_transaction(portfolio) -> Generator:
    """
    Транзакция портфеля: при успехе — commit, при исключении — rollback.
    """
    portfolio.save_snapshot()
    try:
        yield portfolio
        portfolio.clear_snapshot()
    except Exception:
        portfolio.restore_snapshot()
        raise


@contextmanager
def temporary_price(portfolio, ticker: str, price: float) -> Generator[None, None, None]:
    """Временно подменяет цену инструмента, затем восстанавливает."""
    old_price = portfolio.get_price(ticker)
    portfolio.update_price(ticker, price)
    try:
        yield
    finally:
        portfolio.update_price(ticker, old_price)


@contextmanager
def suppress_and_log(
    *exc_types: Type[BaseException],
    log_prefix: str = "[suppress]",
) -> Generator[None, None, None]:
    """Подавляет указанные исключения и пишет в лог."""
    try:
        yield
    except exc_types as e:
        logger.warning("%s %s: %s", log_prefix, type(e).__name__, e)
        print(f"{log_prefix} подавлено: {type(e).__name__}: {e}")
