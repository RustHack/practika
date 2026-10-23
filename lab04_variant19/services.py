"""Бизнес-логика."""

from __future__ import annotations

from typing import List

from exceptions import InvalidPropertyDataError, PropertyNotFoundError
from models import Property
from storage import export_csv, load_json, save_json


class PropertyService:
    def __init__(self) -> None:
        self._properties: List[Property] = load_json()
        self._next_id = self._calc_next_id()

    def _calc_next_id(self) -> int:
        if not self._properties:
            return 1
        ids = [p.id for p in self._properties if p.id is not None]
        return max(ids) + 1 if ids else 1

    def _save(self) -> None:
        save_json(self._properties)

    def add(
        self,
        address: str,
        property_type: str,
        area: float,
        rooms: int,
        price: float,
    ) -> Property:
        """Добавление объекта."""
        if not address.strip():
            raise InvalidPropertyDataError("Адрес не может быть пустым")
        if area <= 0:
            raise InvalidPropertyDataError("Площадь должна быть положительной")
        if rooms < 0:
            raise InvalidPropertyDataError("Количество комнат не может быть отрицательным")
        if price < 0:
            raise InvalidPropertyDataError("Стоимость не может быть отрицательной")

        prop = Property(
            address=address.strip(),
            property_type=property_type.strip().lower(),
            area=area,
            rooms=rooms,
            price=price,
            property_id=self._next_id,
        )
        self._properties.append(prop)
        self._next_id += 1
        self._save()
        return prop

    def get_all(self) -> List[Property]:
        """Все объекты."""
        return list(self._properties)

    def find_by_id(self, property_id: int) -> Property:
        """Поиск по ID."""
        for prop in self._properties:
            if prop.id == property_id:
                return prop
        raise PropertyNotFoundError(f"Объект с ID {property_id} не найден")

    def update_price(self, property_id: int, new_price: float) -> Property:
        """Изменение стоимости."""
        if new_price < 0:
            raise InvalidPropertyDataError("Стоимость не может быть отрицательной")
        prop = self.find_by_id(property_id)
        prop.price = new_price
        self._save()
        return prop

    def filter_by_type(self, property_type: str) -> List[Property]:
        """Фильтрация по типу."""
        normalized = property_type.strip().lower()
        return [p for p in self._properties if p.property_type == normalized]

    def sort_by_price(self) -> List[Property]:
        """Сортировка по цене (по возрастанию)."""
        return sorted(self._properties, key=lambda p: p.price)

    def export_to_csv(self) -> str:
        """Экспорт в CSV."""
        return export_csv(self._properties)
