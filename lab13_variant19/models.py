"""Документная модель актива (MongoDB-стиль) и кэш котировок (Redis-стиль)."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class Asset:
    """Документ актива в «коллекции» portfolio."""
    ticker: str
    name: str
    asset_class: str
    quantity: float
    avg_price: float
    _id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_doc(self) -> Dict[str, Any]:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        return d

    @classmethod
    def from_doc(cls, doc: Dict[str, Any]) -> "Asset":
        doc = dict(doc)
        if isinstance(doc.get("created_at"), str):
            doc["created_at"] = datetime.fromisoformat(doc["created_at"])
        return cls(**{k: v for k, v in doc.items() if k in cls.__dataclass_fields__})


class MongoStore:
    """Учебная in-memory имитация MongoDB (коллекция documents)."""

    def __init__(self) -> None:
        self._collections: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def insert_one(self, collection: str, doc: Dict[str, Any]) -> str:
        col = self._collections.setdefault(collection, {})
        _id = doc.get("_id") or str(uuid.uuid4())
        doc = dict(doc)
        doc["_id"] = _id
        col[_id] = doc
        return _id

    def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        col = self._collections.get(collection, {})
        for doc in col.values():
            if all(doc.get(k) == v for k, v in query.items()):
                return dict(doc)
        return None

    def find(self, collection: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        col = self._collections.get(collection, {})
        query = query or {}
        result = []
        for doc in col.values():
            if all(doc.get(k) == v for k, v in query.items()):
                result.append(dict(doc))
        return result

    def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        doc = self.find_one(collection, query)
        if not doc:
            return False
        col = self._collections[collection]
        _id = doc["_id"]
        col[_id].update(update.get("$set", update))
        return True

    def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        doc = self.find_one(collection, query)
        if not doc:
            return False
        del self._collections[collection][doc["_id"]]
        return True


class RedisCache:
    """Учебная in-memory имитация Redis с TTL."""

    def __init__(self) -> None:
        self._data: Dict[str, tuple] = {}  # key -> (value, expire_at|None)

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        expire_at = time.time() + ex if ex else None
        self._data[key] = (value, expire_at)

    def get(self, key: str) -> Optional[Any]:
        item = self._data.get(key)
        if item is None:
            return None
        value, expire_at = item
        if expire_at is not None and time.time() > expire_at:
            del self._data[key]
            return None
        return value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def exists(self, key: str) -> bool:
        return self.get(key) is not None
