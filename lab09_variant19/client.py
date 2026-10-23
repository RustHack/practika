"""
TCP-клиент биржевых заявок.
Запуск: python client.py (после server.py)
"""

from __future__ import annotations

import socket

from protocol import encode, recv_message

HOST, PORT = "127.0.0.1", 9090


class Client:
    def __init__(self) -> None:
        self.sock: socket.socket | None = None

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        print(f"Подключено к {HOST}:{PORT}")

    def close(self) -> None:
        if self.sock:
            self.sock.close()
            self.sock = None

    def request(self, msg: dict) -> dict:
        assert self.sock
        self.sock.sendall(encode(msg))
        resp = recv_message(self.sock)
        if resp is None:
            raise ConnectionError("Сервер закрыл соединение")
        return resp


def print_orders(data: list) -> None:
    if not data:
        print("  (пусто)")
        return
    for o in data:
        print(
            f"  [{o['id']}] {o['side'].upper()} {o['ticker']} | "
            f"{o['quantity']} x {o['price']} = {o['amount']:,.2f} | {o['status']}"
        )


def main() -> None:
    client = Client()
    try:
        client.connect()
    except ConnectionRefusedError:
        print("Сервер не запущен. Сначала: python server.py")
        return

    while True:
        print("\n===== БИРЖЕВЫЕ ЗАЯВКИ TCP (ЛР9, вар.19) =====")
        print("1. Все заявки")
        print("2. Активные заявки")
        print("3. Заявка по ID")
        print("4. Создать заявку")
        print("5. Отменить заявку")
        print("6. Исполнить заявку")
        print("7. Объём активных (portfolio_value)")
        print("8. Фильтр по тикеру")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            r = client.request({"action": "list_orders"})
            print_orders(r.get("data", []) if r["status"] == "ok" else [])
            if r["status"] != "ok":
                print("Ошибка:", r.get("message"))

        elif choice == "2":
            r = client.request({"action": "list_active"})
            if r["status"] == "ok":
                print_orders(r["data"])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "3":
            oid = int(input("ID: ").strip())
            r = client.request({"action": "get_order", "id": oid})
            if r["status"] == "ok":
                print_orders([r["data"]])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "4":
            ticker = input("Тикер: ").strip()
            side = input("Сторона (buy/sell): ").strip()
            price = float(input("Цена: ").replace(",", "."))
            qty = int(input("Количество: "))
            r = client.request({
                "action": "create_order",
                "ticker": ticker, "side": side,
                "price": price, "quantity": qty,
            })
            if r["status"] == "ok":
                print("Создана:")
                print_orders([r["data"]])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "5":
            oid = int(input("ID: ").strip())
            r = client.request({"action": "cancel_order", "id": oid})
            if r["status"] == "ok":
                print_orders([r["data"]])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "6":
            oid = int(input("ID: ").strip())
            r = client.request({"action": "fill_order", "id": oid})
            if r["status"] == "ok":
                print_orders([r["data"]])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "7":
            r = client.request({"action": "portfolio_value"})
            if r["status"] == "ok":
                print(f"Объём активных заявок: {r['data']['active_volume']:,.2f}")
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "8":
            ticker = input("Тикер: ").strip()
            r = client.request({"action": "filter_by_ticker", "ticker": ticker})
            if r["status"] == "ok":
                print_orders(r["data"])
            else:
                print("Ошибка:", r.get("message"))

        elif choice == "0":
            client.close()
            print("Выход.")
            break
        else:
            print("Неизвестный пункт")


if __name__ == "__main__":
    main()
