"""Демонстрация Django-моделей портфеля (без полного Django runtime)."""
from portfolio.models import PortfolioStore

def main():
    store = PortfolioStore()
    print("Инвесторы:", store.investors)
    print("Активы:", store.assets)
    print("Стоимость портфеля:", store.portfolio_value(1))
    t = store.buy(1, 1, 10, 285.0)
    print("Сделка:", t)
    print("Новая стоимость:", store.portfolio_value(1))
    print("История:", store.transactions)

if __name__ == "__main__":
    main()
