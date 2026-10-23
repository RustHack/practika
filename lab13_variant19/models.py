"""Документная модель актива (MongoDB-стиль) и кэш котировок (Redis-стиль)."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional
import copy

@dataclass
class Asset:
    ticker: str
    name: str
    asset_type: str
    exchange: str
    quantity: float
    price: float
    history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

class MongoStore:
    def __init__(self) -> None:
        self._docs: Dict[str, dict] = {}

    def insert(self, asset: Asset) -> dict:
        d = asset.to_dict()
        d["_id"] = asset.ticker
        d["updated_at"] = datetime.utcnow().isoformat()
        self._docs[asset.ticker] = d
        return copy.deepcopy(d)

    def find(self, ticker: str) -> Optional[dict]:
        d = self._docs.get(ticker.upper())
        return copy.deepcopy(d) if d else None

    def find_all(self, asset_type: str | None = None) -> List[dict]:
        items = list(self._docs.values())
        if asset_type:
            items = [x for x in items if x["asset_type"] == asset_type]
        return copy.deepcopy(items)

    def update(self, ticker: str, **fields) -> Optional[dict]:
        d = self._docs.get(ticker.upper())
        if not d:
            return None
        for k, v in fields.items():
            if k in d and k != "_id":
                d[k] = v
        d["updated_at"] = datetime.utcnow().isoformat()
        return copy.deepcopy(d)

    def delete(self, ticker: str) -> bool:
        return self._docs.pop(ticker.upper(), None) is not None

class RedisCache:
    def __init__(self) -> None:
        self._kv: Dict[str, Any] = {}
        self._scores: Dict[str, float] = {}

    def set(self, key: str, value: Any) -> None:
        self._kv[key] = value

    def get(self, key: str) -> Any:
        return self._kv.get(key)

    def delete(self, key: str) -> None:
        self._kv.pop(key, None)

    def zadd(self, member: str, score: float) -> None:
        self._scores[member] = score

    def zrevrange(self, n: int = 5) -> List[tuple]:
        return sorted(self._scores.items(), key=lambda x: -x[1])[:n]
