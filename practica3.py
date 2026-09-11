from abc import ABC, abstractmethod


class Property(ABC):
    """Базовый класс объекта недвижимости"""

    def __init__(self, address: str, area: float, base_price_per_m2: float):
        self.address = address
        self.area = area                    # площадь в м²
        self.base_price_per_m2 = base_price_per_m2  # базовая цена аренды за м²

    @abstractmethod
    def calculate_rent(self) -> float:
        """Абстрактный метод расчёта стоимости аренды"""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.address}, {self.area} м²"


class Apartment(Property):
    """Квартира"""

    def __init__(self, address: str, area: float, base_price_per_m2: float, rooms: int):
        super().__init__(address, area, base_price_per_m2)
        self.rooms = rooms

    def calculate_rent(self) -> float:
        """
        Стоимость аренды квартиры:
        базовая цена * площадь * коэффициент количества комнат
        """
        # Коэффициент: 1 комната — 1.0, 2 — 1.15, 3 — 1.3, 4+ — 1.4
        if self.rooms == 1:
            coeff = 1.0
        elif self.rooms == 2:
            coeff = 1.15
        elif self.rooms == 3:
            coeff = 1.3
        else:
            coeff = 1.4

        return self.area * self.base_price_per_m2 * coeff

    def __str__(self):
        return (f"Квартира: {self.address} | "
                f"{self.area} м² | {self.rooms} комн. | "
                f"Аренда: {self.calculate_rent():,.0f} руб./мес.")


class Office(Property):
    """Офис"""

    def __init__(self, address: str, area: float, base_price_per_m2: float, workplaces: int):
        super().__init__(address, area, base_price_per_m2)
        self.workplaces = workplaces

    def calculate_rent(self) -> float:
        """
        Стоимость аренды офиса:
        базовая цена * площадь + доплата за каждое рабочее место
        """
        workplace_fee = 3500  # доплата за одно рабочее место
        return self.area * self.base_price_per_m2 + self.workplaces * workplace_fee

    def __str__(self):
        return (f"Офис: {self.address} | "
                f"{self.area} м² | {self.workplaces} раб. мест | "
                f"Аренда: {self.calculate_rent():,.0f} руб./мес.")


class RealEstateAgency:
    """Агентство недвижимости"""

    def __init__(self, name: str):
        self.name = name
        self.properties: list[Property] = []

    def add_property(self, prop: Property):
        """Добавить объект"""
        self.properties.append(prop)

    def remove_property(self, prop: Property):
        """Удалить объект"""
        if prop in self.properties:
            self.properties.remove(prop)

    def total_rent(self) -> float:
        """Суммарная стоимость аренды всех объектов"""
        return sum(p.calculate_rent() for p in self.properties)

    def average_rent(self) -> float:
        """Средняя стоимость аренды"""
        if not self.properties:
            return 0.0
        return self.total_rent() / len(self.properties)

    def find_by_address(self, address_part: str) -> list[Property]:
        """Поиск по части адреса"""
        address_part = address_part.lower()
        return [p for p in self.properties if address_part in p.address.lower()]

    def filter_by_type(self, prop_type: type) -> list[Property]:
        """Фильтрация по типу (Apartment или Office)"""
        return [p for p in self.properties if isinstance(p, prop_type)]

    def most_expensive(self) -> Property | None:
        """Самый дорогой объект по аренде"""
        if not self.properties:
            return None
        return max(self.properties, key=lambda p: p.calculate_rent())

    def show_all(self):
        """Вывести все объекты"""
        print(f"\n{'='*70}")
        print(f"Агентство: {self.name}")
        print(f"{'='*70}")
        if not self.properties:
            print("Нет объектов")
            return
        for i, prop in enumerate(self.properties, 1):
            print(f"{i}. {prop}")
        print("-" * 70)
        print(f"Всего объектов: {len(self.properties)}")
        print(f"Суммарная аренда: {self.total_rent():,.0f} руб./мес.")
        print(f"Средняя аренда:   {self.average_rent():,.0f} руб./мес.")


# ==================== Демонстрация ====================
if __name__ == "__main__":
    agency = RealEstateAgency("Городская недвижимость")

    # Добавляем квартиры
    agency.add_property(Apartment("ул. Ленина, 15, кв. 42", 45, 800, 1))
    agency.add_property(Apartment("пр. Мира, 28, кв. 17", 68, 950, 2))
    agency.add_property(Apartment("ул. Гагарина, 5, кв. 9", 92, 1100, 3))
    agency.add_property(Apartment("ул. Советская, 101, кв. 3", 120, 1300, 4))

    # Добавляем офисы
    agency.add_property(Office("БЦ «Север», этаж 4", 80, 1500, 10))
    agency.add_property(Office("БЦ «Центр», этаж 7", 150, 1800, 25))
    agency.add_property(Office("ул. Промышленная, 12", 60, 1200, 8))

    # Вывод всех объектов
    agency.show_all()

    # Примеры использования методов агентства
    print("\n--- Квартиры ---")
    for apt in agency.filter_by_type(Apartment):
        print(apt)

    print("\n--- Самый дорогой объект ---")
    print(agency.most_expensive())

    print("\n--- Поиск по адресу 'Ленина' ---")
    for p in agency.find_by_address("Ленина"):
        print(p)