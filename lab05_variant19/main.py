#!/usr/bin/env python3
"""
Лабораторная работа 5. Функциональное программирование.
Вариант 19 — инвестиционный портфель / торговля.
map, filter, reduce, lambda, partial, comprehensions.
"""
from functools import reduce, partial
from operator import attrgetter, itemgetter
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime, date
import statistics


@dataclass
class Instrument:
    ticker: str
    name: str
    asset_class: str  # stock, bond, etf, crypto
    sector: str
    price: float
    volume: int = 0


@dataclass
class Position:
    instrument: Instrument
    quantity: float
    avg_price: float
    current_price: float

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.avg_price

    @property
    def pnl(self) -> float:
        return self.market_value - self.cost_basis

    @property
    def pnl_pct(self) -> float:
        if self.cost_basis == 0:
            return 0.0
        return (self.pnl / self.cost_basis) * 100


@dataclass
class Trade:
    ticker: str
    side: str  # buy / sell
    quantity: float
    price: float
    timestamp: datetime
    commission: float = 0.0

    @property
    def notional(self) -> float:
        return self.quantity * self.price


def create_sample_instruments() -> List[Instrument]:
    return [
        Instrument("SBER", "Сбербанк", "stock", "finance", 285.40, 1_500_000),
        Instrument("GAZP", "Газпром", "stock", "energy", 158.20, 2_100_000),
        Instrument("LKOH", "Лукойл", "stock", "energy", 7120.0, 120_000),
        Instrument("YNDX", "Яндекс", "stock", "tech", 3840.0, 80_000),
        Instrument("TCSG", "TCS Group", "stock", "finance", 2890.0, 45_000),
        Instrument("FXGD", "FinEx Gold", "etf", "commodities", 1420.5, 30_000),
        Instrument("FXUS", "FinEx USA", "etf", "equity", 5890.0, 25_000),
        Instrument("OFZ", "ОФЗ 26238", "bond", "gov", 98.45, 500_000),
        Instrument("BTC", "Bitcoin", "crypto", "crypto", 4_250_000.0, 150),
        Instrument("ETH", "Ethereum", "crypto", "crypto", 215_000.0, 800),
    ]


def create_sample_positions(instruments: List[Instrument]) -> List[Position]:
    by_ticker = {i.ticker: i for i in instruments}
    data = [
        ("SBER", 100, 270.0, 285.40),
        ("GAZP", 200, 165.0, 158.20),
        ("LKOH", 5, 6800.0, 7120.0),
        ("YNDX", 10, 3600.0, 3840.0),
        ("FXGD", 20, 1350.0, 1420.5),
        ("BTC", 0.05, 3_800_000.0, 4_250_000.0),
    ]
    return [
        Position(by_ticker[t], q, ap, cp)
        for t, q, ap, cp in data
    ]


def create_sample_trades() -> List[Trade]:
    now = datetime.now()
    return [
        Trade("SBER", "buy", 50, 268.0, now, 15.0),
        Trade("SBER", "buy", 50, 272.0, now, 15.0),
        Trade("GAZP", "buy", 200, 165.0, now, 20.0),
        Trade("LKOH", "buy", 5, 6800.0, now, 50.0),
        Trade("YNDX", "buy", 10, 3600.0, now, 30.0),
        Trade("FXGD", "buy", 20, 1350.0, now, 10.0),
        Trade("BTC", "buy", 0.05, 3_800_000.0, now, 100.0),
        Trade("GAZP", "sell", 50, 160.0, now, 10.0),
    ]


def demo_map_filter_reduce():
    print("=" * 60)
    print("1. map / filter / reduce")
    print("=" * 60)
    instruments = create_sample_instruments()
    positions = create_sample_positions(instruments)
    trades = create_sample_trades()

    # map: извлечь тикеры
    tickers = list(map(attrgetter("ticker"), instruments))
    print("Тикеры (map):", tickers)

    # map: рыночная стоимость позиций
    values = list(map(lambda p: p.market_value, positions))
    print("Стоимости позиций:", [round(v, 2) for v in values])

    # filter: только акции
    stocks = list(filter(lambda i: i.asset_class == "stock", instruments))
    print("Акции:", [i.ticker for i in stocks])

    # filter: прибыльные позиции
    profitable = list(filter(lambda p: p.pnl > 0, positions))
    print("Прибыльные:", [(p.instrument.ticker, round(p.pnl, 2)) for p in profitable])

    # reduce: суммарная стоимость портфеля
    total_value = reduce(lambda acc, p: acc + p.market_value, positions, 0.0)
    print(f"Суммарная стоимость: {total_value:,.2f}")

    # reduce: суммарный PnL
    total_pnl = reduce(lambda acc, p: acc + p.pnl, positions, 0.0)
    print(f"Суммарный PnL: {total_pnl:,.2f}")

    # filter + map + reduce: комиссия по покупкам
    buy_commission = reduce(
        lambda a, t: a + t.commission,
        filter(lambda t: t.side == "buy", trades),
        0.0,
    )
    print(f"Комиссия по покупкам: {buy_commission:.2f}")


def demo_comprehensions():
    print("\n" + "=" * 60)
    print("2. List / dict / set comprehensions")
    print("=" * 60)
    instruments = create_sample_instruments()
    positions = create_sample_positions(instruments)

    # list comp: тикеры с ценой > 1000
    expensive = [i.ticker for i in instruments if i.price > 1000]
    print("Дорогие инструменты:", expensive)

    # dict comp: ticker -> price
    price_map = {i.ticker: i.price for i in instruments}
    print("Цена SBER:", price_map.get("SBER"))

    # set comp: уникальные сектора
    sectors = {i.sector for i in instruments}
    print("Сектора:", sectors)

    # nested: группировка по классу актива
    by_class: Dict[str, List[str]] = {}
    for i in instruments:
        by_class.setdefault(i.asset_class, []).append(i.ticker)
    # через comprehension
    classes = {c: [i.ticker for i in instruments if i.asset_class == c]
               for c in {i.asset_class for i in instruments}}
    print("По классам:", classes)

    # PnL в процентах
    pnl_pcts = {p.instrument.ticker: round(p.pnl_pct, 2) for p in positions}
    print("PnL %:", pnl_pcts)


def demo_partial_and_higher_order():
    print("\n" + "=" * 60)
    print("3. partial и функции высшего порядка")
    print("=" * 60)
    instruments = create_sample_instruments()

    def filter_by_class(items: List[Instrument], asset_class: str) -> List[Instrument]:
        return list(filter(lambda i: i.asset_class == asset_class, items))

    filter_stocks = partial(filter_by_class, asset_class="stock")
    filter_crypto = partial(filter_by_class, asset_class="crypto")

    print("Акции (partial):", [i.ticker for i in filter_stocks(instruments)])
    print("Крипто (partial):", [i.ticker for i in filter_crypto(instruments)])

    def apply_to_prices(items: List[Instrument], fn: Callable[[float], float]) -> List[float]:
        return list(map(lambda i: fn(i.price), items))

    # наценка 1%
    marked = apply_to_prices(instruments, lambda p: round(p * 1.01, 2))
    print("Цены +1%:", marked[:5], "...")

    # статистика
    prices = list(map(attrgetter("price"), instruments))
    print(f"Средняя цена: {statistics.mean(prices):,.2f}")
    print(f"Медиана: {statistics.median(prices):,.2f}")


def demo_pipeline():
    print("\n" + "=" * 60)
    print("4. Конвейер обработки сделок")
    print("=" * 60)
    trades = create_sample_trades()

    # pipeline: только buy -> notional -> sum
    total_bought = reduce(
        lambda acc, n: acc + n,
        map(
            lambda t: t.notional,
            filter(lambda t: t.side == "buy", trades),
        ),
        0.0,
    )
    print(f"Объём покупок: {total_bought:,.2f}")

    # группировка по тикеру (функциональный стиль)
    def group_by_ticker(ts: List[Trade]) -> Dict[str, List[Trade]]:
        return reduce(
            lambda acc, t: {**acc, t.ticker: acc.get(t.ticker, []) + [t]},
            ts,
            {},
        )

    grouped = group_by_ticker(trades)
    for ticker, ts in grouped.items():
        vol = sum(t.quantity for t in ts)
        print(f"  {ticker}: {len(ts)} сделок, объём {vol}")


def main():
    print("Лабораторная 5 — Функциональное программирование")
    print("Вариант 19: инвестиционный портфель / торговля\n")
    demo_map_filter_reduce()
    demo_comprehensions()
    demo_partial_and_higher_order()
    demo_pipeline()
    print("\nГотово.")


if __name__ == "__main__":
    main()
