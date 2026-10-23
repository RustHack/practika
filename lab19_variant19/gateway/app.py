"""API Gateway (порт 8000)."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, urllib.request

def get(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())

class H(BaseHTTPRequestHandler):
    def _j(self, c, d):
        b = json.dumps(d, ensure_ascii=False).encode()
        self.send_response(c)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        try:
            if self.path == "/api/portfolio":
                users = get("http://127.0.0.1:8001/users")
                assets = get("http://127.0.0.1:8002/assets")
                self._j(200, {"users": users, "assets": assets})
            elif self.path == "/health":
                self._j(200, {"status": "ok"})
            else:
                self._j(404, {"error": "not found"})
        except Exception as e:
            self._j(502, {"error": str(e)})
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("gateway :8000")
    HTTPServer(("127.0.0.1", 8000), H).serve_forever()
