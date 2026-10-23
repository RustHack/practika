"""Прикладной протокол: 8-байтный заголовок длины + JSON."""

from __future__ import annotations

import json
from typing import Any


def encode(message: dict[str, Any]) -> bytes:
    payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
    return f"{len(payload):08d}".encode("ascii") + payload


def recv_message(sock) -> dict[str, Any] | None:
    header = b""
    while len(header) < 8:
        chunk = sock.recv(8 - len(header))
        if not chunk:
            return None
        header += chunk
    length = int(header.decode("ascii"))
    body = b""
    while len(body) < length:
        chunk = sock.recv(length - len(body))
        if not chunk:
            return None
        body += chunk
    return json.loads(body.decode("utf-8"))
