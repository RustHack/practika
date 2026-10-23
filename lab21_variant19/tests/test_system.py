import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.service import TradingSystem

def test_buy_and_value():
    s = TradingSystem()
    s.buy(1, "SBER", 10)
    assert s.portfolios[1].positions["SBER"] == 10
    assert abs(s.value(1) - 100_000) < 0.01

def test_insufficient():
    s = TradingSystem()
    try:
        s.buy(1, "SBER", 10_000)
        assert False
    except ValueError:
        pass

def test_sell():
    s = TradingSystem()
    s.buy(1, "GAZP", 10)
    s.sell(1, "GAZP", 5)
    assert s.portfolios[1].positions["GAZP"] == 5
