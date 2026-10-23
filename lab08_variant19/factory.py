"""Паттерн Factory."""

from __future__ import annotations

from models import Bond, Fund, Instrument, Stock


class InstrumentFactory:
    """Фабрика финансовых инструментов."""

    _next_id: int = 1

    @classmethod
    def create(cls, instrument_type: str, **kwargs) -> Instrument:
        instrument_type = instrument_type.lower().strip()
        iid = cls._next_id
        cls._next_id += 1

        if instrument_type in ("stock", "акция"):
            return Stock(
                id=iid,
                ticker=kwargs["ticker"].upper(),
                name=kwargs["name"],
                price=kwargs["price"],
                quantity=kwargs.get("quantity", 0),
                dividend_yield=kwargs.get("dividend_yield", 0.0),
            )
        if instrument_type in ("bond", "облигация"):
            return Bond(
                id=iid,
                ticker=kwargs["ticker"].upper(),
                name=kwargs["name"],
                price=kwargs["price"],
                quantity=kwargs.get("quantity", 0),
                coupon_rate=kwargs.get("coupon_rate", 0.0),
                nominal=kwargs.get("nominal", 1000.0),
            )
        if instrument_type in ("fund", "фонд"):
            return Fund(
                id=iid,
                ticker=kwargs["ticker"].upper(),
                name=kwargs["name"],
                price=kwargs["price"],
                quantity=kwargs.get("quantity", 0),
                management_fee=kwargs.get("management_fee", 1.0),
            )
        raise ValueError(f"Неизвестный тип инструмента: {instrument_type}")
