"""Минимум 10 тестов для Lab 11."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from db import init_db, get_connection, DB_PATH
from repository import OrderRepository
from service import OrderService


def setup_module():
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()


def test_init_has_seed_data():
    with get_connection() as conn:
        n = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert n >= 10


def test_create_order():
    repo = OrderRepository()
    o = repo.create(1, 1, "buy", 100.0, 10)
    assert o["id"] > 0
    assert o["ticker"] == "SBER"


def test_get_order():
    repo = OrderRepository()
    o = repo.get_by_id(1)
    assert o is not None
    assert "ticker" in o


def test_get_missing():
    repo = OrderRepository()
    assert repo.get_by_id(99999) is None


def test_list_filter_status():
    repo = OrderRepository()
    active = repo.list_all(status="active")
    assert all(o["status"] == "active" for o in active)


def test_update_status():
    repo = OrderRepository()
    o = repo.create(1, 2, "sell", 50.0, 5)
    updated = repo.update_status(o["id"], "filled")
    assert updated["status"] == "filled"


def test_delete():
    repo = OrderRepository()
    o = repo.create(1, 1, "buy", 10.0, 1)
    assert repo.delete(o["id"]) is True
    assert repo.get_by_id(o["id"]) is None


def test_active_volume():
    repo = OrderRepository()
    v = repo.active_volume()
    assert v >= 0


def test_stats():
    repo = OrderRepository()
    stats = repo.stats_by_ticker()
    assert len(stats) >= 1
    assert "ticker" in stats[0]


def test_transaction_transfer():
    repo = OrderRepository()
    n = repo.transfer_orders(1, 2)
    assert n >= 0


def test_service_cache_get():
    svc = OrderService()
    o1 = svc.get_order(1)
    o2 = svc.get_order(1)
    assert o1 == o2


def test_service_create_invalid_side():
    import sqlite3
    svc = OrderService()
    try:
        svc.create_order(1, 1, "hold", 1.0, 1)
        assert False
    except (ValueError, sqlite3.IntegrityError):
        pass
