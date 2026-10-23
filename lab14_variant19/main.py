"""
ЛР14 — FastAPI REST API, вариант 19: инвестиционный портфель (/assets).
Запуск: uvicorn main:app --reload --port 8000
"""
from __future__ import annotations
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Portfolio API", version="1.0")

class AssetIn(BaseModel):
    ticker: str
    name: str
    asset_type: str = Field(description="stock|bond|fund")
    exchange: str = "MOEX"
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    yield_pct: float = 0.0
    risk: float = 0.0

class Asset(AssetIn):
    id: int

_db: list[Asset] = []
_next = 1

def seed():
    global _next
    if _db:
        return
    for a in [
        AssetIn(ticker="SBER", name="Сбербанк", asset_type="stock", quantity=100, price=280.5, yield_pct=8, risk=0.7),
        AssetIn(ticker="GAZP", name="Газпром", asset_type="stock", quantity=50, price=160, yield_pct=6, risk=0.6),
        AssetIn(ticker="OFZ26238", name="ОФЗ", asset_type="bond", quantity=10, price=980, yield_pct=7, risk=0.15),
        AssetIn(ticker="FXUS", name="FinEx USA", asset_type="fund", quantity=5, price=5500, yield_pct=5, risk=0.4),
    ]:
        _db.append(Asset(id=_next, **a.model_dump()))
        _next += 1

@app.on_event("startup")
def on_start():
    seed()

@app.get("/assets", response_model=List[Asset])
def list_assets(asset_type: Optional[str] = None):
    items = _db
    if asset_type:
        items = [a for a in items if a.asset_type == asset_type]
    return items

@app.get("/assets/{asset_id}", response_model=Asset)
def get_asset(asset_id: int):
    for a in _db:
        if a.id == asset_id:
            return a
    raise HTTPException(404, "Asset not found")

@app.post("/assets", response_model=Asset, status_code=201)
def create_asset(data: AssetIn):
    global _next
    a = Asset(id=_next, **data.model_dump())
    _next += 1
    _db.append(a)
    return a

@app.put("/assets/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, data: AssetIn):
    for i, a in enumerate(_db):
        if a.id == asset_id:
            updated = Asset(id=asset_id, **data.model_dump())
            _db[i] = updated
            return updated
    raise HTTPException(404, "Asset not found")

@app.patch("/assets/{asset_id}", response_model=Asset)
def patch_asset(asset_id: int, price: Optional[float] = None, quantity: Optional[float] = None):
    for a in _db:
        if a.id == asset_id:
            if price is not None:
                a.price = price
            if quantity is not None:
                a.quantity = quantity
            return a
    raise HTTPException(404, "Asset not found")

@app.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int):
    for i, a in enumerate(_db):
        if a.id == asset_id:
            _db.pop(i)
            return
    raise HTTPException(404, "Asset not found")

@app.get("/assets/stats/summary")
def stats():
    if not _db:
        return {"portfolio_value": 0, "avg_yield": 0, "by_type": {}}
    total = sum(a.quantity * a.price for a in _db)
    avg_y = sum(a.yield_pct for a in _db) / len(_db)
    by_type: dict = {}
    for a in _db:
        by_type[a.asset_type] = by_type.get(a.asset_type, 0) + a.quantity * a.price
    return {"portfolio_value": total, "avg_yield": round(avg_y, 2), "by_type": by_type}
