"""
REST API + SQLite + Cache.
Запуск: python server.py
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from db import init_db
from service import OrderService

init_db()
service = OrderService()
STATIC = Path(__file__).parent / "static"


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

        if path.startswith("/static/"):
            name = path[len("/static/"):]
            fpath = STATIC / name
            if fpath.is_file():
                data = fpath.read_bytes()
                self.send_response(200)
                ctype = "text/css" if name.endswith(".css") else (
                    "application/javascript" if name.endswith(".js") else "text/plain"
                )
                self.send_header("Content-Type", ctype)
                self.send_header("Cache-Control", "public, max-age=3600")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self._json(404, {"error": "file not found"})
            return

        if path == "/orders/stats":
            self._json(200, service.stats())
            return
        if path == "/orders/volume":
            self._json(200, {"active_volume": service.active_volume()})
            return
        if path == "/orders":
            status = qs.get("status", [None])[0]
            ticker = qs.get("ticker", [None])[0]
            self._json(200, service.list_orders(status=status, ticker=ticker))
            return
        if path.startswith("/orders/"):
            try:
                oid = int(path.rsplit("/", 1)[-1])
                order = service.get_order(oid)
                if order is None:
                    self._json(404, {"error": "not found"})
                else:
                    self._json(200, order)
            except ValueError:
                self._json(400, {"error": "bad id"})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if path == "/orders":
            try:
                b = self._body()
                order = service.create_order(
                    int(b["trader_id"]), int(b["instrument_id"]),
                    b["side"], float(b["price"]), int(b["quantity"]),
                )
                self._json(201, order)
            except (KeyError, ValueError, TypeError) as e:
                self._json(400, {"error": str(e)})
            return
        if path == "/orders/transfer":
            try:
                b = self._body()
                n = service.transfer(int(b["from_trader"]), int(b["to_trader"]))
                self._json(200, {"transferred": n})
            except (KeyError, ValueError, TypeError) as e:
                self._json(400, {"error": str(e)})
            return
        self._json(404, {"error": "not found"})

    def do_PATCH(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if path.startswith("/orders/") and path.endswith("/status"):
            try:
                oid = int(path.split("/")[2])
                b = self._body()
                order = service.update_status(oid, b["status"])
                self._json(200, order)
            except KeyError as e:
                self._json(404, {"error": str(e)})
            except (ValueError, TypeError) as e:
                self._json(400, {"error": str(e)})
            return
        self._json(404, {"error": "not found"})

    def do_DELETE(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        if path.startswith("/orders/"):
            try:
                oid = int(path.rsplit("/", 1)[-1])
                service.delete_order(oid)
                self.send_response(204)
                self.end_headers()
            except KeyError as e:
                self._json(404, {"error": str(e)})
            except ValueError:
                self._json(400, {"error": "bad id"})
            return
        self._json(404, {"error": "not found"})


def main() -> None:
    STATIC.mkdir(parents=True, exist_ok=True)
    (STATIC / "style.css").write_text("body { font-family: sans-serif; }", encoding="utf-8")
    (STATIC / "app.js").write_text("console.log('trading app');", encoding="utf-8")
    (STATIC / "readme.txt").write_text("Static demo for CDN section", encoding="utf-8")

    httpd = HTTPServer(("127.0.0.1", 8000), Handler)
    print("Lab 11 API  http://127.0.0.1:8000")
    print("  GET  /orders  /orders/{id}  /orders/stats  /orders/volume")
    print("  POST /orders  /orders/transfer")
    print("  PATCH /orders/{id}/status")
    print("  DELETE /orders/{id}")
    print("  GET  /static/style.css  (Cache-Control: max-age=3600)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСтоп")
        httpd.server_close()


if __name__ == "__main__":
    main()
