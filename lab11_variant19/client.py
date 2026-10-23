"""HTTP-клиент для Lab 11."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

BASE = "http://127.0.0.1:8000"


def api(method: str, path: str, data: dict | None = None):
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {"error": "http error"}


def main() -> None:
    try:
        api("GET", "/orders")
    except urllib.error.URLError:
        print("Сервер не запущен: python server.py")
        return

    while True:
        print("\n===== TRADING DB (ЛР11, вар.19) =====")
        print("1. Список заявок")
        print("2. Заявка по ID")
        print("3. Создать заявку")
        print("4. Изменить статус")
        print("5. Удалить")
        print("6. Статистика по тикерам")
        print("7. Объём активных")
        print("8. Перенос заявок (транзакция)")
        print("0. Выход")
        c = input("Выбор: ").strip()

        if c == "1":
            st = input("status (пусто=все): ").strip() or None
            tk = input("ticker (пусто=все): ").strip() or None
            params = {}
            if st:
                params["status"] = st
            if tk:
                params["ticker"] = tk
            qs = ("?" + urlencode(params)) if params else ""
            code, data = api("GET", "/orders" + qs)
            print(f"HTTP {code}, записей: {len(data) if data else 0}")
            for o in (data or [])[:15]:
                print(f"  [{o['id']}] {o['side']} {o['ticker']} "
                      f"{o['quantity']}x{o['price']} {o['status']} ({o['trader_name']})")

        elif c == "2":
            i = input("ID: ").strip()
            code, data = api("GET", f"/orders/{i}")
            print(f"HTTP {code}: {data}")

        elif c == "3":
            tid = int(input("trader_id: "))
            iid = int(input("instrument_id: "))
            side = input("side buy/sell: ").strip()
            price = float(input("price: ").replace(",", "."))
            qty = int(input("quantity: "))
            code, data = api("POST", "/orders", {
                "trader_id": tid, "instrument_id": iid,
                "side": side, "price": price, "quantity": qty,
            })
            print(f"HTTP {code}: {data}")

        elif c == "4":
            i = input("ID: ").strip()
            st = input("status: ").strip()
            code, data = api("PATCH", f"/orders/{i}/status", {"status": st})
            print(f"HTTP {code}: {data}")

        elif c == "5":
            i = input("ID: ").strip()
            code, data = api("DELETE", f"/orders/{i}")
            print(f"HTTP {code}")

        elif c == "6":
            code, data = api("GET", "/orders/stats")
            print(f"HTTP {code}")
            for s in data or []:
                print(f"  {s['ticker']}: orders={s['orders_count']} "
                      f"active={s['active_count']} volume={s['total_volume']:,.0f}")

        elif c == "7":
            code, data = api("GET", "/orders/volume")
            print(f"HTTP {code}: {data}")

        elif c == "8":
            a = int(input("from_trader: "))
            b = int(input("to_trader: "))
            code, data = api("POST", "/orders/transfer", {
                "from_trader": a, "to_trader": b,
            })
            print(f"HTTP {code}: {data}")

        elif c == "0":
            break
        else:
            print("?")


if __name__ == "__main__":
    main()
