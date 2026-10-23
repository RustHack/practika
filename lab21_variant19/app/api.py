from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from app.service import TradingSystem

system = TradingSystem()

class Handler(BaseHTTPRequestHandler):
    def _j(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_GET(self):
        if self.path == "/health":
            self._j(200, {"status": "ok"})
        elif self.path == "/portfolio/1":
            p = system.portfolios[1]
            self._j(200, {"cash": p.cash, "positions": p.positions, "value": system.value(1)})
        elif self.path == "/trades":
            self._j(200, [t.__dict__ for t in system.trades])
        else:
            self._j(404, {"error": "not found"})

    def do_POST(self):
        try:
            b = self._body()
            if self.path == "/buy":
                t = system.buy(int(b["user_id"]), b["ticker"], float(b["qty"]))
                self._j(201, t.__dict__)
            elif self.path == "/sell":
                t = system.sell(int(b["user_id"]), b["ticker"], float(b["qty"]))
                self._j(201, t.__dict__)
            else:
                self._j(404, {"error": "not found"})
        except (KeyError, ValueError) as e:
            self._j(400, {"error": str(e)})

    def log_message(self, *a):
        pass

def main():
    print("Final project API :8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

if __name__ == "__main__":
    main()
