"""Модель объекта недвижимости."""

from __future__ import annotations
from typing import Any


class Property:
    """Объект недвижимости."""

    def __init__(
        self,
        address: str,
        property_type: str,
        area: float,
        rooms: int,
        price: float,
        property_id: int | None = None,
    ) -> None:
        self.id = property_id
        self.address = address
        self.property_type = property_type
        self.area = area
        self.rooms = rooms
        self.price = price

    def to_dict(self) -> dict[str, Any]:
        """Преобразование объекта в словарь."""
        return {
            "id": self.id,
            "address": self.address,
            "property_type": self.property_type,
            "area": self.area,
            "rooms": self.rooms,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Property:
        """Создание объекта из словаря."""
        return cls(
            address=data["address"],
            property_type=data["property_type"],
            area=data["area"],
            rooms=data["rooms"],
            price=data["price"],
            property_id=data.get("id"),
        )

    def __str__(self) -> str:
        return (
            f"[ID: {self.id}] {self.address} | "
            f"тип: {self.property_type} | "
            f"площадь: {self.area} м² | "
            f"комнат: {self.rooms} | "
            f"цена: {self.price:,.0f} руб."
        )
