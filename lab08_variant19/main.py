"""
Лабораторная работа №8 — Вариант 19.
Инвестиционный портфель (Factory, Strategy, Observer).
"""

from __future__ import annotations

from models import Bond, Fund, Stock
from observers import ConsoleObserver, LogObserver
from services import PortfolioService


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Ошибка: введите число")


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число")


def print_instr(instr) -> None:
    kind = type(instr).__name__
    print(
        f"  [ID:{instr.id}] {instr.ticker} ({kind}) | {instr.name} | "
        f"цена: {instr.price:,.2f} | кол-во: {instr.quantity} | "
        f"стоимость: {instr.value:,.2f}"
    )


def main() -> None:
    service = PortfolioService()
    service.attach(ConsoleObserver())
    service.attach(LogObserver())

    service.add_instrument("stock", ticker="SBER", name="Сбербанк", price=280.0, quantity=10, dividend_yield=8.0)
    service.add_instrument("bond", ticker="OFZ26238", name="ОФЗ 26238", price=980.0, quantity=5, coupon_rate=7.1, nominal=1000.0)
    service.add_instrument("fund", ticker="FXUS", name="FinEx USA", price=5500.0, quantity=2, management_fee=0.9)

    print("Демо-данные загружены.\n")

    while True:
        print("===== ПОРТФЕЛЬ (ЛР8, вар.19) =====")
        print("1. Показать инструменты")
        print("2. Добавить акцию (Factory)")
        print("3. Добавить облигацию (Factory)")
        print("4. Добавить фонд (Factory)")
        print("5. Стоимость портфеля (Strategy)")
        print("6. Доходность портфеля (Strategy)")
        print("7. Риск портфеля (Strategy)")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        try:
            if choice == "1":
                print("\n--- Инструменты ---")
                items = service.get_all()
                if not items:
                    print("  (пусто)")
                for i in items:
                    print_instr(i)

            elif choice == "2":
                t = input("Тикер: ").strip()
                n = input("Название: ").strip()
                p = input_float("Цена: ")
                q = input_int("Количество: ")
                d = input_float("Див. доходность (%): ")
                instr = service.add_instrument("stock", ticker=t, name=n, price=p, quantity=q, dividend_yield=d)
                print_instr(instr)

            elif choice == "3":
                t = input("Тикер: ").strip()
                n = input("Название: ").strip()
                p = input_float("Цена: ")
                q = input_int("Количество: ")
                c = input_float("Купон (%): ")
                nom = input_float("Номинал: ")
                instr = service.add_instrument("bond", ticker=t, name=n, price=p, quantity=q, coupon_rate=c, nominal=nom)
                print_instr(instr)

            elif choice == "4":
                t = input("Тикер: ").strip()
                n = input("Название: ").strip()
                p = input_float("Цена: ")
                q = input_int("Количество: ")
                fee = input_float("Комиссия (%): ")
                instr = service.add_instrument("fund", ticker=t, name=n, price=p, quantity=q, management_fee=fee)
                print_instr(instr)

            elif choice == "5":
                val = service.portfolio_value()
                print(f"\nСтоимость портфеля: {val:,.2f} руб.")

            elif choice == "6":
                yld = service.portfolio_yield()
                print(f"\nДоходность портфеля: {yld:,.2f} руб.")

            elif choice == "7":
                risk = service.portfolio_risk()
                print(f"\nРиск портфеля: {risk}%")

            elif choice == "0":
                print("Выход.")
                break

            else:
                print("Неизвестный пункт")

        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
