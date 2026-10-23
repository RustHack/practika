"""ЛР18 — pytest + unittest.mock, вариант 19: биржевой симулятор."""
import pytest
from unittest.mock import Mock
from portfolio import Portfolio, StaticQuotes

@pytest.fixture
def quotes():
    return StaticQuotes({"SBER": 100.0, "GAZP": 50.0})

@pytest.fixture
def portfolio(quotes):
    return Portfolio(cash=1000.0, quotes=quotes)

def test_create_portfolio(portfolio):
    assert portfolio.cash == 1000
    assert portfolio.positions == {}

def test_buy(portfolio):
    portfolio.buy("SBER", 2)
    assert portfolio.positions["SBER"] == 2
    assert portfolio.cash == 800

def test_sell(portfolio):
    portfolio.buy("SBER", 5)
    portfolio.sell("SBER", 2)
    assert portfolio.positions["SBER"] == 3
    assert portfolio.cash == 700

def test_value(portfolio):
    portfolio.buy("SBER", 2)
    portfolio.buy("GAZP", 2)
    assert portfolio.value() == 1000

def test_insufficient_funds(portfolio):
    with pytest.raises(ValueError, match="средств"):
        portfolio.buy("SBER", 100)

def test_insufficient_shares(portfolio):
    with pytest.raises(ValueError, match="бумаг"):
        portfolio.sell("SBER", 1)

def test_unknown_ticker(portfolio):
    with pytest.raises(KeyError):
        portfolio.buy("XXXX", 1)

def test_mock_quotes():
    mock = Mock()
    mock.get_price.return_value = 200.0
    p = Portfolio(1000, mock)
    p.buy("SBER", 2)
    mock.get_price.assert_called_with("SBER")
    assert p.cash == 600

def test_mock_price_change():
    mock = Mock()
    mock.get_price.side_effect = [100.0, 150.0]
    p = Portfolio(1000, mock)
    p.buy("SBER", 2)
    assert p.value() == 800 + 2 * 150

@pytest.mark.parametrize("qty,ok", [(1, True), (10, True), (11, False)])
def test_param_buy(qty, ok):
    q = StaticQuotes({"SBER": 100.0})
    p = Portfolio(1000, q)
    if ok:
        p.buy("SBER", qty)
        assert p.positions["SBER"] == qty
    else:
        with pytest.raises(ValueError):
            p.buy("SBER", qty)
