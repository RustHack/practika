"""API портфеля для контейнеризации."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

PORT = int(os.environ.get("PORT", 8000))
ASSETS = [{"ticker": "SBER", "qty": 100, "price": 280.5}]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ok"}'
        elif self.path == "/assets":
            body = json.dumps(ASSETS).encode()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print(f"listening {PORT}")
    HTTPServer(("0.0.0.0", PORT), H).serve_forever()
