#!/usr/bin/env python3
"""
Лабораторная работа 6. Декораторы и контекстные менеджеры.
Вариант 19 — инвестиционный портфель / торговля.
"""
from __future__ import annotations

import time
from typing import List

from models import Instrument, Position, Order, OrderSide, OrderStatus
from services import PortfolioService, OrderService
from decorators import (
    timer,
    retry,
    log_calls,
    validate_positive,
    cache_result,
)
from context import portfolio_transaction, temporary_price, suppress_and_log


def seed_instruments() -> List[Instrument]:
    return [
        Instrument("SBER", "Сбербанк", "stock", 285.40),
        Instrument("GAZP", "Газпром", "stock", 158.20),
        Instrument("LKOH", "Лукойл", "stock", 7120.0),
        Instrument("YNDX", "Яндекс", "stock", 3840.0),
        Instrument("FXGD", "FinEx Gold", "etf", 1420.5),
        Instrument("BTC", "Bitcoin", "crypto", 4_250_000.0),
    ]


@timer
@log_calls
def build_demo_portfolio(svc: PortfolioService) -> None:
    instruments = seed_instruments()
    for inst in instruments:
        svc.add_instrument(inst)

    svc.open_position("SBER", 100, 270.0)
    svc.open_position("GAZP", 200, 165.0)
    svc.open_position("LKOH", 5, 6800.0)
    svc.open_position("YNDX", 10, 3600.0)
    svc.open_position("FXGD", 20, 1350.0)
    svc.open_position("BTC", 0.05, 3_800_000.0)


@retry(max_attempts=3, delay=0.1)
@validate_positive("quantity", "price")
def place_safe_order(order_svc: OrderService, ticker: str, side: OrderSide,
                     quantity: float, price: float) -> Order:
    return order_svc.place_order(ticker, side, quantity, price)


@cache_result(ttl=5.0)
def expensive_portfolio_value(svc: PortfolioService) -> float:
    """Имитация тяжёлого расчёта — кэшируется."""
    time.sleep(0.05)
    return svc.total_value()


def demo_decorators():
    print("=" * 60)
    print("1. Декораторы")
    print("=" * 60)

    portfolio = PortfolioService()
    orders = OrderService(portfolio)

    build_demo_portfolio(portfolio)
    print(f"Позиций: {len(portfolio.positions)}")
    print(f"Стоимость: {portfolio.total_value():,.2f}")

    # timer + log_calls уже отработали на build_demo_portfolio

    # retry + validate
    try:
        place_safe_order(orders, "SBER", OrderSide.BUY, -10, 280.0)
    except ValueError as e:
        print(f"Валидация сработала: {e}")

    order = place_safe_order(orders, "SBER", OrderSide.BUY, 10, 280.0)
    print(f"Ордер размещён: {order}")

    # cache
    t0 = time.perf_counter()
    v1 = expensive_portfolio_value(portfolio)
    t1 = time.perf_counter()
    v2 = expensive_portfolio_value(portfolio)
    t2 = time.perf_counter()
    print(f"Первый вызов value={v1:,.2f} за {(t1-t0)*1000:.1f} мс")
    print(f"Второй (кэш) value={v2:,.2f} за {(t2-t1)*1000:.1f} мс")


def demo_context_managers():
    print("\n" + "=" * 60)
    print("2. Контекстные менеджеры")
    print("=" * 60)

    portfolio = PortfolioService()
    for inst in seed_instruments():
        portfolio.add_instrument(inst)
    portfolio.open_position("SBER", 100, 270.0)
    portfolio.open_position("GAZP", 200, 165.0)

    print(f"До транзакции: value={portfolio.total_value():,.2f}")

    # успешная транзакция
    with portfolio_transaction(portfolio) as p:
        p.open_position("LKOH", 2, 7100.0)
        p.update_price("SBER", 290.0)
    print(f"После успешной: value={portfolio.total_value():,.2f}, "
          f"позиций={len(portfolio.positions)}")

    # откат при ошибке
    try:
        with portfolio_transaction(portfolio) as p:
            p.open_position("YNDX", 5, 3800.0)
            raise RuntimeError("Имитация сбоя")
    except RuntimeError:
        print("Ошибка поймана, откат выполнен")
    print(f"После отката: value={portfolio.total_value():,.2f}, "
          f"позиций={len(portfolio.positions)}")

    # temporary_price
    with temporary_price(portfolio, "SBER", 300.0):
        print(f"Временная цена SBER: {portfolio.get_price('SBER')}")
        print(f"Value внутри: {portfolio.total_value():,.2f}")
    print(f"Цена после выхода: {portfolio.get_price('SBER')}")

    # suppress_and_log
    with suppress_and_log(ValueError, log_prefix="[demo]"):
        raise ValueError("Эта ошибка будет подавлена")
    print("Продолжили после suppress_and_log")


def demo_combined():
    print("\n" + "=" * 60)
    print("3. Совместное использование")
    print("=" * 60)

    portfolio = PortfolioService()
    orders = OrderService(portfolio)
    for inst in seed_instruments():
        portfolio.add_instrument(inst)

    with portfolio_transaction(portfolio):
        portfolio.open_position("SBER", 50, 280.0)
        portfolio.open_position("BTC", 0.01, 4_000_000.0)

    @timer
    def rebalance():
        with portfolio_transaction(portfolio):
            # продаём часть SBER, покупаем GAZP
            place_safe_order(orders, "SBER", OrderSide.SELL, 20, 285.0)
            place_safe_order(orders, "GAZP", OrderSide.BUY, 50, 158.0)

    rebalance()
    print(f"После ребалансировки: value={portfolio.total_value():,.2f}")
    for pos in portfolio.positions:
        print(f"  {pos}")


def main():
    print("Лабораторная 6 — Декораторы и контекстные менеджеры")
    print("Вариант 19: инвестиционный портфель / торговля\n")
    demo_decorators()
    demo_context_managers()
    demo_combined()
    print("\nГотово.")


if __name__ == "__main__":
    main()
