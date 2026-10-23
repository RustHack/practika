"""Паттерн Strategy."""

from __future__ import annotations

from typing import List, Protocol

from models import Bond, Fund, Instrument, Stock


class CalculationStrategy(Protocol):
    def calculate(self, instruments: List[Instrument]) -> float: ...


class ValueStrategy:
    def calculate(self, instruments: List[Instrument]) -> float:
        return sum(i.value for i in instruments)


class YieldStrategy:
    def calculate(self, instruments: List[Instrument]) -> float:
        total = 0.0
        for i in instruments:
            if isinstance(i, Stock):
                total += i.value * i.dividend_yield / 100
            elif isinstance(i, Bond):
                total += i.quantity * i.nominal * i.coupon_rate / 100
            elif isinstance(i, Fund):
                total += i.value * (5.0 - i.management_fee) / 100
        return total


class RiskStrategy:
    def calculate(self, instruments: List[Instrument]) -> float:
        if not instruments:
            return 0.0
        risk = 0.0
        total_value = sum(i.value for i in instruments) or 1
        for i in instruments:
            weight = i.value / total_value
            if isinstance(i, Stock):
                risk += weight * 0.7
            elif isinstance(i, Bond):
                risk += weight * 0.15
            elif isinstance(i, Fund):
                risk += weight * 0.4
        return round(risk * 100, 2)
