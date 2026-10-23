"""ЛР18 — pytest + unittest.mock, вариант 19: биржевой симулятор."""
import pytest
from unittest.mock import Mock, patch
from portfolio import Portfolio, StaticQuotes


@pytest.fixture
def quotes():
    return StaticQuotes({"SBER": 285.4, "GAZP": 158.2, "LKOH": 7120.0})


@pytest.fixture
def portfolio(quotes):
    p = Portfolio(quotes)
    p.buy("SBER", 100, 270.0)
    p.buy("GAZP", 200, 165.0)
    return p


def test_buy_creates_position(portfolio):
    assert "SBER" in portfolio.positions
    assert portfolio.positions["SBER"].quantity == 100
    assert portfolio.positions["SBER"].avg_price == 270.0


def test_total_value(portfolio):
    # SBER 100*285.4 + GAZP 200*158.2
    expected = 100 * 285.4 + 200 * 158.2
    assert abs(portfolio.total_value() - expected) < 0.01


def test_pnl(portfolio):
    # SBER: (285.4-270)*100 = 1540; GAZP: (158.2-165)*200 = -1360
    expected = 1540 + (-1360)
    assert abs(portfolio.total_pnl() - expected) < 0.01


def test_sell_reduces_quantity(portfolio):
    portfolio.sell("SBER", 40)
    assert portfolio.positions["SBER"].quantity == 60


def test_sell_all_removes_position(portfolio):
    portfolio.sell("GAZP", 200)
    assert "GAZP" not in portfolio.positions


def test_sell_too_much_raises(portfolio):
    with pytest.raises(ValueError):
        portfolio.sell("SBER", 999)


def test_buy_unknown_ticker_raises(quotes):
    p = Portfolio(quotes)
    with pytest.raises(KeyError):
        p.buy("UNKNOWN", 10, 100.0)


@patch("portfolio.StaticQuotes.get")
def test_mock_quote(mock_get, portfolio):
    mock_get.return_value = 300.0
    # подмена котировки через mock на уровне quotes
    portfolio.quotes.get = mock_get
    val = portfolio.positions["SBER"].quantity * portfolio.quotes.get("SBER")
    assert val == 100 * 300.0
    mock_get.assert_called_with("SBER")


def test_mock_portfolio_service():
    """Пример мока внешнего сервиса."""
    mock_svc = Mock()
    mock_svc.get_price.return_value = 290.0
    mock_svc.place_order.return_value = {"status": "filled", "id": 42}

    price = mock_svc.get_price("SBER")
    order = mock_svc.place_order("SBER", "buy", 10, price)

    assert price == 290.0
    assert order["status"] == "filled"
    mock_svc.get_price.assert_called_once_with("SBER")
    mock_svc.place_order.assert_called_once()
