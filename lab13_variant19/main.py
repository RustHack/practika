"""ЛР13 — MongoDB + Redis (учебные in-memory реализации), вариант 19."""
from service import PortfolioService

def main():
    svc = PortfolioService()
    print("=== Портфель (MongoDB + Redis) ===\n")
    for a in svc.list_assets():
        print(f"  {a['ticker']}: {a['quantity']} x {a['price']} ({a['asset_type']})")
    print(f"\nСтоимость: {svc.portfolio_value():,.2f}")
    print(f"Котировка SBER (Redis): {svc.quote('SBER')}")
    print("Рейтинг активов:", svc.ranking())
    svc.update_price("SBER", 290.0)
    svc.redis.delete("calc:portfolio_value")
    print(f"После обновления SBER: {svc.portfolio_value():,.2f}")

if __name__ == "__main__":
    main()
