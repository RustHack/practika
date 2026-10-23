"""Тесты Lab 12 — SQLAlchemy."""

from pathlib import Path
import pytest

DB = Path("/tmp/lab12_trading.db")
if DB.exists():
    DB.unlink()

from database import init_db, get_session
from models import Order, Trader
from repository import OrderRepository
from service import OrderService
from sqlalchemy import select


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_seed_traders():
    with get_session() as s:
        n = len(s.scalars(select(Trader)).all())
    assert n >= 2


def test_create_order():
    svc = OrderService()
    o = svc.create(1, 1, "buy", 100.0, 10)
    assert o.id > 0


def test_get_order():
    svc = OrderService()
    o = svc.create(1, 2, "sell", 50.0, 5)
    got = svc.get(o.id)
    assert got.side == "sell"
    assert got.instrument.ticker == "GAZP"


def test_get_missing():
    svc = OrderService()
    with pytest.raises(KeyError):
        svc.get(99999)


def test_list_filter():
    svc = OrderService()
    active = svc.list(status="active")
    assert all(o.status == "active" for o in active)


def test_update_status():
    svc = OrderService()
    o = svc.create(1, 1, "buy", 10.0, 1)
    u = svc.set_status(o.id, "filled")
    assert u.status == "filled"


def test_delete():
    svc = OrderService()
    o = svc.create(1, 1, "buy", 10.0, 1)
    svc.delete(o.id)
    with pytest.raises(KeyError):
        svc.get(o.id)


def test_sort_price():
    svc = OrderService()
    orders = svc.list(sort_price=True, desc=True)
    prices = [o.price for o in orders]
    assert prices == sorted(prices, reverse=True)


def test_trader_relation():
    svc = OrderService()
    orders = svc.trader_orders(1)
    assert len(orders) >= 1


def test_active_volume():
    svc = OrderService()
    assert svc.active_volume() >= 0


def test_transfer_transaction():
    svc = OrderService()
    n = svc.transfer(1, 2)
    assert n >= 0


def test_invalid_side():
    svc = OrderService()
    with pytest.raises(ValueError):
        svc.create(1, 1, "hold", 1.0, 1)
