# ЛР19 — Микросервисы (вариант 19: портфель)

Сервисы:
- users_service :8001
- assets_service :8002 (+ события asset.created)
- gateway :8000 → GET /api/portfolio

```bash
python users_service/app.py
python assets_service/app.py
python gateway/app.py
```
