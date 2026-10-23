"""Микросервис пользователей (порт 8001)."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

USERS = {1: {"id": 1, "name": "Иванов", "email": "ivanov@mail.ru"}}

class H(BaseHTTPRequestHandler):
    def _j(self, c, d):
        b = json.dumps(d, ensure_ascii=False).encode()
        self.send_response(c)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        if self.path == "/users":
            self._j(200, list(USERS.values()))
        elif self.path.startswith("/users/"):
            uid = int(self.path.rsplit("/", 1)[-1])
            self._j(200, USERS[uid]) if uid in USERS else self._j(404, {"error": "not found"})
        else:
            self._j(404, {"error": "not found"})
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("users :8001")
    HTTPServer(("127.0.0.1", 8001), H).serve_forever()
