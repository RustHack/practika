"""
Лабораторная работа №12 — Вариант 19.
SQLAlchemy ORM: биржевые заявки.
"""

from __future__ import annotations

from database import init_db
from service import OrderService


def print_order(o) -> None:
    ticker = o.instrument.ticker if o.instrument else "?"
    trader = o.trader.name if o.trader else "?"
    print(
        f"  [{o.id}] {o.side.upper()} {ticker} | "
        f"{o.quantity} x {o.price} = {o.amount:,.2f} | "
        f"{o.status} | {trader}"
    )


def main() -> None:
    init_db()
    svc = OrderService()
    print("БД инициализирована (SQLAlchemy ORM)\n")

    while True:
        print("===== ORM TRADING (ЛР12, вар.19) =====")
        print("1. Список заявок")
        print("2. Заявка по ID")
        print("3. Создать")
        print("4. Изменить статус")
        print("5. Удалить")
        print("6. Фильтр по статусу")
        print("7. Сортировка по цене")
        print("8. Заявки трейдера (связь)")
        print("9. Объём активных")
        print("10. Перенос заявок (транзакция)")
        print("0. Выход")
        c = input("Выбор: ").strip()

        try:
            if c == "1":
                for o in svc.list():
                    print_order(o)
            elif c == "2":
                oid = int(input("ID: "))
                print_order(svc.get(oid))
            elif c == "3":
                tid = int(input("trader_id: "))
                iid = int(input("instrument_id: "))
                side = input("side: ").strip()
                price = float(input("price: ").replace(",", "."))
                qty = int(input("quantity: "))
                o = svc.create(tid, iid, side, price, qty)
                print("Создана:")
                print_order(svc.get(o.id))
            elif c == "4":
                oid = int(input("ID: "))
                st = input("status: ").strip()
                print_order(svc.set_status(oid, st))
            elif c == "5":
                oid = int(input("ID: "))
                svc.delete(oid)
                print("Удалено")
            elif c == "6":
                st = input("status: ").strip()
                for o in svc.list(status=st):
                    print_order(o)
            elif c == "7":
                desc = input("по убыванию? (y/n): ").strip().lower() == "y"
                for o in svc.list(sort_price=True, desc=desc):
                    print_order(o)
            elif c == "8":
                tid = int(input("trader_id: "))
                for o in svc.trader_orders(tid):
                    print_order(o)
            elif c == "9":
                print(f"Объём активных: {svc.active_volume():,.2f}")
            elif c == "10":
                a = int(input("from_trader: "))
                b = int(input("to_trader: "))
                n = svc.transfer(a, b)
                print(f"Перенесено: {n}")
            elif c == "0":
                break
            else:
                print("?")
        except (ValueError, KeyError) as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
