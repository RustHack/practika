"""
TCP-сервер биржевых заявок.
Запуск: python server.py
"""

from __future__ import annotations

import socket
import threading

from models import OrderService
from protocol import encode, recv_message

HOST, PORT = "127.0.0.1", 9090


def order_to_dict(o) -> dict:
    return {
        "id": o.id,
        "ticker": o.ticker,
        "side": o.side,
        "price": o.price,
        "quantity": o.quantity,
        "status": o.status,
        "amount": o.amount,
    }


class Server:
    def __init__(self) -> None:
        self.service = OrderService()

    def handle(self, req: dict) -> dict:
        action = req.get("action")
        try:
            if action == "list_orders":
                return {"status": "ok", "data": [order_to_dict(o) for o in self.service.list_orders()]}

            if action == "list_active":
                return {"status": "ok", "data": [order_to_dict(o) for o in self.service.list_active()]}

            if action == "get_order":
                o = self.service.get_order(int(req["id"]))
                if o is None:
                    return {"status": "error", "message": "Заявка не найдена"}
                return {"status": "ok", "data": order_to_dict(o)}

            if action == "create_order":
                o = self.service.create_order(
                    req["ticker"], req["side"], float(req["price"]), int(req["quantity"])
                )
                return {"status": "ok", "data": order_to_dict(o)}

            if action == "cancel_order":
                o = self.service.cancel_order(int(req["id"]))
                return {"status": "ok", "data": order_to_dict(o)}

            if action == "fill_order":
                o = self.service.fill_order(int(req["id"]))
                return {"status": "ok", "data": order_to_dict(o)}

            if action == "portfolio_value":
                value = self.service.portfolio_value()
                return {"status": "ok", "data": {"active_volume": value}}

            if action == "filter_by_ticker":
                orders = self.service.filter_by_ticker(req["ticker"])
                return {"status": "ok", "data": [order_to_dict(o) for o in orders]}

            return {"status": "error", "message": f"Неизвестное действие: {action}"}
        except (ValueError, KeyError, TypeError) as e:
            return {"status": "error", "message": str(e)}

    def client_thread(self, conn: socket.socket, addr: tuple) -> None:
        print(f"[+] {addr}")
        try:
            while True:
                req = recv_message(conn)
                if req is None:
                    break
                print(f"  <- {req.get('action')}")
                conn.sendall(encode(self.handle(req)))
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            conn.close()
            print(f"[-] {addr}")

    def run(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"TCP-сервер биржевых заявок {HOST}:{PORT}")
        try:
            while True:
                conn, addr = sock.accept()
                threading.Thread(target=self.client_thread, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nСтоп")
        finally:
            sock.close()


if __name__ == "__main__":
    Server().run()
