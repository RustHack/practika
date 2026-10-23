"""
REST API биржевых заявок.
Запуск: python server.py
http://127.0.0.1:8000
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from models import OrderService

service = OrderService()


class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, data) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}

    def log_message(self, fmt, *args) -> None:
        print(f"  {self.command} {self.path} -> {args[1]}")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        qs = parse_qs(parsed.query)

        if path == "/orders/active":
            self._json(200, [o.to_dict() for o in service.list_active()])
            return

        if path == "/orders/volume":
            self._json(200, {"active_volume": service.active_volume()})
            return

        if path == "/orders":
            ticker = qs.get("ticker", [None])[0]
            side = qs.get("side", [None])[0]
            status = qs.get("status", [None])[0]
            data = service.list(ticker=ticker, side=side, status=status)
            self._json(200, [o.to_dict() for o in data])
            return

        if path.startswith("/orders/"):
            try:
                oid = int(path.rsplit("/", 1)[-1])
                order = service.get(oid)
                self._json(200, order.to_dict())
            except ValueError:
                self._json(400, {"error": "Некорректный ID", "code": "BAD_ID"})
            except KeyError as e:
                self._json(404, {"error": str(e), "code": "NOT_FOUND"})
            return

        self._json(404, {"error": "Не найден", "code": "NOT_FOUND"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if path != "/orders":
            self._json(404, {"error": "Не найден", "code": "NOT_FOUND"})
            return
        try:
            body = self._body()
            order = service.create(
                body["ticker"], body["side"],
                float(body["price"]), int(body["quantity"]),
            )
            self._json(201, order.to_dict())
        except (KeyError, ValueError, TypeError) as e:
            self._json(400, {"error": str(e), "code": "BAD_REQUEST"})

    def do_PUT(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if not path.startswith("/orders/"):
            self._json(404, {"error": "Не найден", "code": "NOT_FOUND"})
            return
        try:
            oid = int(path.rsplit("/", 1)[-1])
            body = self._body()
            order = service.update(
                oid,
                ticker=body["ticker"],
                side=body["side"],
                price=body["price"],
                quantity=body["quantity"],
                status=body.get("status", "active"),
            )
            self._json(200, order.to_dict())
        except ValueError as e:
            self._json(400, {"error": str(e), "code": "BAD_REQUEST"})
        except KeyError as e:
            self._json(404, {"error": str(e), "code": "NOT_FOUND"})

    def do_PATCH(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if not path.startswith("/orders/"):
            self._json(404, {"error": "Не найден", "code": "NOT_FOUND"})
            return
        try:
            oid = int(path.rsplit("/", 1)[-1])
            body = self._body()
            order = service.update(oid, **body)
            self._json(200, order.to_dict())
        except ValueError as e:
            self._json(400, {"error": str(e), "code": "BAD_REQUEST"})
        except KeyError as e:
            self._json(404, {"error": str(e), "code": "NOT_FOUND"})

    def do_DELETE(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if not path.startswith("/orders/"):
            self._json(404, {"error": "Не найден", "code": "NOT_FOUND"})
            return
        try:
            oid = int(path.rsplit("/", 1)[-1])
            service.delete(oid)
            self.send_response(204)
            self.end_headers()
        except ValueError:
            self._json(400, {"error": "Некорректный ID", "code": "BAD_ID"})
        except KeyError as e:
            self._json(404, {"error": str(e), "code": "NOT_FOUND"})


def main() -> None:
    httpd = HTTPServer(("127.0.0.1", 8000), Handler)
    print("REST API биржевых заявок  http://127.0.0.1:8000")
    print("  GET    /orders")
    print("  GET    /orders?ticker=SBER&side=buy&status=active")
    print("  GET    /orders/{id}")
    print("  GET    /orders/active")
    print("  GET    /orders/volume")
    print("  POST   /orders")
    print("  PUT    /orders/{id}")
    print("  PATCH  /orders/{id}")
    print("  DELETE /orders/{id}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСтоп")
        httpd.server_close()


if __name__ == "__main__":
    main()
