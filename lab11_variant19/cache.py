"""Простой кэш: Redis если доступен, иначе in-memory с TTL."""

from __future__ import annotations

import json
import time
from typing import Any, Optional


class MemoryCache:
    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float | None]] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if item is None:
            return None
        value, expires = item
        if expires is not None and time.time() > expires:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int | None = 60) -> None:
        expires = time.time() + ttl if ttl else None
        self._store[key] = (value, expires)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


def create_cache():
    try:
        import redis
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()

        class RedisCache:
            def __init__(self, client):
                self._r = client

            def get(self, key: str):
                data = self._r.get(key)
                return json.loads(data) if data else None

            def set(self, key: str, value, ttl: int | None = 60):
                self._r.set(key, json.dumps(value, ensure_ascii=False), ex=ttl)

            def delete(self, key: str):
                self._r.delete(key)

            def clear(self):
                self._r.flushdb()

        print("[cache] Redis подключён")
        return RedisCache(r)
    except Exception:
        print("[cache] Redis недоступен, используется MemoryCache")
        return MemoryCache()
