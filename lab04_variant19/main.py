"""
Лабораторная работа №4 — Вариант 19.
Система управления объектами недвижимости.
"""

from __future__ import annotations

from exceptions import InvalidPropertyDataError, PropertyNotFoundError
from services import PropertyService


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


def print_properties(properties: list) -> None:
    if not properties:
        print("  (пусто)")
        return
    for prop in properties:
        print(f"  {prop}")


def main() -> None:
    service = PropertyService()
    print(f"Загружено объектов: {len(service.get_all())}")

    while True:
        print("\n===== МЕНЮ =====")
        print("1. Добавить объект")
        print("2. Показать все")
        print("3. Поиск по ID")
        print("4. Изменить стоимость")
        print("5. Фильтрация по типу")
        print("6. Сортировка по цене")
        print("7. Экспорт в CSV")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            print("\n--- Добавление ---")
            address = input("Адрес: ").strip()
            property_type = input("Тип: ").strip()
            area = input_float("Площадь (м²): ")
            rooms = input_int("Количество комнат: ")
            price = input_float("Стоимость (руб.): ")
            try:
                prop = service.add(address, property_type, area, rooms, price)
                print(f"Добавлено:\n  {prop}")
            except InvalidPropertyDataError as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            print("\n--- Все объекты ---")
            print_properties(service.get_all())

        elif choice == "3":
            print("\n--- Поиск ---")
            prop_id = input_int("ID: ")
            try:
                prop = service.find_by_id(prop_id)
                print(f"Найден:\n  {prop}")
            except PropertyNotFoundError as e:
                print(f"Ошибка: {e}")

        elif choice == "4":
            print("\n--- Изменение стоимости ---")
            prop_id = input_int("ID: ")
            new_price = input_float("Новая стоимость: ")
            try:
                prop = service.update_price(prop_id, new_price)
                print(f"Обновлено:\n  {prop}")
            except (PropertyNotFoundError, InvalidPropertyDataError) as e:
                print(f"Ошибка: {e}")

        elif choice == "5":
            print("\n--- Фильтрация ---")
            ptype = input("Тип: ").strip()
            results = service.filter_by_type(ptype)
            print(f"Найдено: {len(results)}")
            print_properties(results)

        elif choice == "6":
            print("\n--- Сортировка по цене ---")
            print_properties(service.sort_by_price())

        elif choice == "7":
            path = service.export_to_csv()
            print(f"Экспортировано в: {path}")

        elif choice == "0":
            print("Выход. Данные сохранены.")
            break

        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
