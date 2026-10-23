"""Микросервис активов (порт 8002)."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

ASSETS = [
    {"id": 1, "ticker": "SBER", "price": 280.5, "owner_id": 1},
    {"id": 2, "ticker": "GAZP", "price": 160.0, "owner_id": 1},
]
EVENTS = []

class H(BaseHTTPRequestHandler):
    def _j(self, c, d):
        b = json.dumps(d, ensure_ascii=False).encode()
        self.send_response(c)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}
    def do_GET(self):
        if self.path == "/assets":
            self._j(200, ASSETS)
        elif self.path == "/events":
            self._j(200, EVENTS)
        else:
            self._j(404, {"error": "not found"})
    def do_POST(self):
        if self.path == "/assets":
            a = self._body()
            a["id"] = len(ASSETS) + 1
            ASSETS.append(a)
            EVENTS.append({"type": "asset.created", "asset_id": a["id"]})
            self._j(201, a)
        else:
            self._j(404, {"error": "not found"})
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("assets :8002")
    HTTPServer(("127.0.0.1", 8002), H).serve_forever()
