from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class User:
    id: int
    name: str

@dataclass
class Asset:
    id: int
    ticker: str
    price: float

@dataclass
class Portfolio:
    user_id: int
    cash: float = 100_000.0
    positions: Dict[str, float] = field(default_factory=dict)

@dataclass
class Trade:
    id: int
    user_id: int
    ticker: str
    side: str
    qty: float
    price: float
