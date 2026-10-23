"""
HTTP-клиент биржевых заявок.
Запуск: python client.py (после server.py)
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

BASE = "http://127.0.0.1:8000"


def api(method: str, path: str, data: dict | None = None) -> tuple[int, dict | list | None]:
    url = BASE + path
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8")
        try:
            return e.code, json.loads(payload)
        except json.JSONDecodeError:
            return e.code, {"error": payload}


def print_orders(data) -> None:
    if not data:
        print("  (пусто)")
        return
    for o in data:
        print(
            f"  [{o['id']}] {o['side'].upper()} {o['ticker']} | "
            f"{o['quantity']} x {o['price']} = {o.get('amount', o['price']*o['quantity']):,.2f} | {o['status']}"
        )


def main() -> None:
    try:
        api("GET", "/orders")
    except urllib.error.URLError:
        print("Сервер не запущен. Сначала: python server.py")
        return

    while True:
        print("\n===== БИРЖЕВЫЕ ЗАЯВКИ REST (ЛР10, вар.19) =====")
        print("1. Список заявок          GET /orders")
        print("2. Фильтр                 GET /orders?ticker=&side=&status=")
        print("3. Заявка по ID           GET /orders/{id}")
        print("4. Создать                POST /orders")
        print("5. Полностью изменить     PUT /orders/{id}")
        print("6. Частично изменить      PATCH /orders/{id}")
        print("7. Удалить                DELETE /orders/{id}")
        print("8. Активные заявки        GET /orders/active")
        print("9. Объём активных         GET /orders/volume")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            code, data = api("GET", "/orders")
            print(f"HTTP {code}")
            print_orders(data)

        elif choice == "2":
            ticker = input("Тикер (пусто = все): ").strip() or None
            side = input("Side buy/sell (пусто = все): ").strip() or None
            status = input("Status (пусто = все): ").strip() or None
            params = {}
            if ticker:
                params["ticker"] = ticker
            if side:
                params["side"] = side
            if status:
                params["status"] = status
            qs = ("?" + urlencode(params)) if params else ""
            code, data = api("GET", "/orders" + qs)
            print(f"HTTP {code}")
            print_orders(data)

        elif choice == "3":
            i = input("ID: ").strip()
            code, data = api("GET", f"/orders/{i}")
            print(f"HTTP {code}: {data}")

        elif choice == "4":
            ticker = input("Тикер: ").strip()
            side = input("Side (buy/sell): ").strip()
            price = float(input("Цена: ").replace(",", "."))
            qty = int(input("Количество: "))
            code, data = api("POST", "/orders", {
                "ticker": ticker, "side": side, "price": price, "quantity": qty,
            })
            print(f"HTTP {code}: {data}")

        elif choice == "5":
            i = input("ID: ").strip()
            ticker = input("Тикер: ").strip()
            side = input("Side: ").strip()
            price = float(input("Цена: ").replace(",", "."))
            qty = int(input("Количество: "))
            status = input("Status: ").strip()
            code, data = api("PUT", f"/orders/{i}", {
                "ticker": ticker, "side": side, "price": price,
                "quantity": qty, "status": status,
            })
            print(f"HTTP {code}: {data}")

        elif choice == "6":
            i = input("ID: ").strip()
            field = input("Поле (status/price/quantity): ").strip()
            value = input("Значение: ").strip()
            if field in ("price",):
                value = float(value.replace(",", "."))
            elif field in ("quantity",):
                value = int(value)
            code, data = api("PATCH", f"/orders/{i}", {field: value})
            print(f"HTTP {code}: {data}")

        elif choice == "7":
            i = input("ID: ").strip()
            code, data = api("DELETE", f"/orders/{i}")
            print(f"HTTP {code}" + (f": {data}" if data else " No Content"))

        elif choice == "8":
            code, data = api("GET", "/orders/active")
            print(f"HTTP {code}")
            print_orders(data)

        elif choice == "9":
            code, data = api("GET", "/orders/volume")
            print(f"HTTP {code}: {data}")

        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неизвестный пункт")


if __name__ == "__main__":
    main()
