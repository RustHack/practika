from __future__ import annotations
from models import Asset, MongoStore, RedisCache

class PortfolioService:
    def __init__(self) -> None:
        self.mongo = MongoStore()
        self.redis = RedisCache()
        for a in [
            Asset("SBER", "Сбербанк", "stock", "MOEX", 100, 280.5, [{"price": 270}, {"price": 280.5}]),
            Asset("GAZP", "Газпром", "stock", "MOEX", 50, 160.0, [{"price": 155}, {"price": 160}]),
            Asset("OFZ26238", "ОФЗ 26238", "bond", "MOEX", 10, 980.0, []),
            Asset("FXUS", "FinEx USA", "fund", "MOEX", 5, 5500.0, []),
        ]:
            self.add_asset(a)

    def add_asset(self, asset: Asset) -> dict:
        doc = self.mongo.insert(asset)
        self.redis.set(f"quote:{asset.ticker}", asset.price)
        self.redis.zadd(asset.ticker, asset.quantity * asset.price)
        return doc

    def get_asset(self, ticker: str) -> dict | None:
        return self.mongo.find(ticker)

    def list_assets(self, asset_type: str | None = None) -> list:
        return self.mongo.find_all(asset_type)

    def update_price(self, ticker: str, price: float) -> dict | None:
        doc = self.mongo.find(ticker)
        if not doc:
            return None
        hist = doc.get("history") or []
        hist.append({"price": price})
        updated = self.mongo.update(ticker, price=price, history=hist)
        self.redis.set(f"quote:{ticker}", price)
        if updated:
            self.redis.zadd(ticker, updated["quantity"] * price)
        return updated

    def quote(self, ticker: str):
        return self.redis.get(f"quote:{ticker.upper()}")

    def ranking(self, n: int = 5):
        return self.redis.zrevrange(n)

    def portfolio_value(self) -> float:
        cached = self.redis.get("calc:portfolio_value")
        if cached is not None:
            return cached
        total = sum(a["quantity"] * a["price"] for a in self.mongo.find_all())
        self.redis.set("calc:portfolio_value", total)
        return total
