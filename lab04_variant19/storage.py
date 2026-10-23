"""Сохранение и загрузка данных."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from models import Property


DATA_DIR = Path(__file__).parent / "data"
JSON_FILE = DATA_DIR / "properties.json"
CSV_FILE = DATA_DIR / "properties.csv"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json() -> List[Property]:
    """Загрузка из JSON. Если файла нет — пустой список."""
    ensure_data_dir()
    if not JSON_FILE.exists():
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Property.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return []


def save_json(properties: List[Property]) -> None:
    """Сохранение в JSON."""
    ensure_data_dir()
    data = [prop.to_dict() for prop in properties]
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def export_csv(properties: List[Property]) -> str:
    """Экспорт в CSV. Возвращает путь к файлу."""
    ensure_data_dir()
    fieldnames = ["id", "address", "property_type", "area", "rooms", "price"]
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prop in properties:
            writer.writerow(prop.to_dict())
    return str(CSV_FILE)
