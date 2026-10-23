"""
Лабораторная работа №7 — Вариант 19.
Инвестиционный портфель (SOLID).
"""

from __future__ import annotations

from models import Bond, Fund, Stock
from notifiers import ConsoleNotifier
from repositories import InMemoryInstrumentRepository
from services import PortfolioService


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Ошибка: введите число")


def print_instr(instr) -> None:
    kind = type(instr).__name__
    print(
        f"  [ID:{instr.id}] {instr.ticker} ({kind}) | {instr.name} | "
        f"цена: {instr.price:,.2f} | кол-во: {instr.quantity} | "
        f"стоимость: {instr.value:,.2f} | прибыль: {instr.calculate_profit():,.2f}"
    )


def main() -> None:
    repo = InMemoryInstrumentRepository()
    notifier = ConsoleNotifier()
    service = PortfolioService(repository=repo, notifier=notifier)

    service.add_stock("SBER", "Сбербанк", 280.0, 10, 8.0)
    service.add_bond("OFZ26238", "ОФЗ 26238", 980.0, 5, 7.1, 1000.0)
    service.add_fund("FXUS", "FinEx USA", 5500.0, 2, 0.9)

    print("Демо-данные загружены.\n")

    while True:
        print("===== ПОРТФЕЛЬ (ЛР7, вар.19) =====")
        print("1. Показать инструменты")
        print("2. Добавить акцию")
        print("3. Добавить облигацию")
        print("4. Добавить фонд")
        print("5. Купить")
        print("6. Продать")
        print("7. Стоимость портфеля")
        print("8. Общая прибыль")
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
                s = service.add_stock(t, n, p, q, d)
                print_instr(s)

            elif choice == "3":
                t = input("Тикер: ").strip()
                n = input("Название: ").strip()
                p = input_float("Цена: ")
                q = input_int("Количество: ")
                c = input_float("Купон (%): ")
                nom = input_float("Номинал: ")
                b = service.add_bond(t, n, p, q, c, nom)
                print_instr(b)

            elif choice == "4":
                t = input("Тикер: ").strip()
                n = input("Название: ").strip()
                p = input_float("Цена: ")
                q = input_int("Количество: ")
                fee = input_float("Комиссия (%): ")
                f = service.add_fund(t, n, p, q, fee)
                print_instr(f)

            elif choice == "5":
                iid = input_int("ID инструмента: ")
                qty = input_int("Количество: ")
                price = input_float("Цена: ")
                service.buy(iid, qty, price)
                print("Покупка выполнена")

            elif choice == "6":
                iid = input_int("ID инструмента: ")
                qty = input_int("Количество: ")
                service.sell(iid, qty)
                print("Продажа выполнена")

            elif choice == "7":
                print(f"\nСтоимость портфеля: {service.portfolio_value():,.2f} руб.")

            elif choice == "8":
                print(f"\nОбщая прибыль: {service.total_profit():,.2f} руб.")

            elif choice == "0":
                print("Выход.")
                break

            else:
                print("Неизвестный пункт")

        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
