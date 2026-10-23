"""ЛР13 — MongoDB + Redis (учебные in-memory реализации), вариант 19."""
from service import PortfolioService
from models import Asset

def main():
    svc = PortfolioService()
    print("=== Портфель (MongoStore + RedisCache) ===")

    a1 = svc.add_asset("SBER", "Сбербанк", "stock", 285.4, 100)
    a2 = svc.add_asset("GAZP", "Газпром", "stock", 158.2, 200)
    a3 = svc.add_asset("BTC", "Bitcoin", "crypto", 4_250_000.0, 0.05)
    print("Добавлены:", a1.ticker, a2.ticker, a3.ticker)

    print("Котировка SBER (кэш):", svc.get_quote("SBER"))
    print("Котировка SBER (повтор, из кэша):", svc.get_quote("SBER"))

    svc.update_quote("SBER", 290.0)
    print("После update SBER:", svc.get_quote("SBER"))

    total = svc.total_value()
    print(f"Стоимость портфеля: {total:,.2f}")

    print("Все активы:", [a.ticker for a in svc.list_assets()])
    print("Готово.")

if __name__ == "__main__":
    main()
