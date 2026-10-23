"""Lab 5 Variant 19 - functional Python for real estate."""
from functools import reduce

properties = [
    {"address": "Lenina 10", "type": "apartment", "area": 45.0, "rooms": 1, "price": 4500000},
    {"address": "Mira 5", "type": "house", "area": 120.0, "rooms": 4, "price": 15000000},
    {"address": "Pobedy 22", "type": "office", "area": 80.0, "rooms": 0, "price": 12000000},
    {"address": "Sadovaya 3", "type": "apartment", "area": 68.5, "rooms": 2, "price": 7200000},
]

def filter_by_area(min_area):
    return list(filter(lambda p: p["area"] >= min_area, properties))

def get_addresses():
    return list(map(lambda p: p["address"], properties))

def sort_by_price():
    return sorted(properties, key=lambda p: p["price"])

def find_most_expensive():
    return reduce(lambda a, b: a if a["price"] > b["price"] else b, properties)

def has_type(t):
    return any(p["type"] == t for p in properties)

def generate_by_rooms(rooms):
    for p in properties:
        if p["rooms"] == rooms:
            yield p

if __name__ == "__main__":
    print("Filtered:", filter_by_area(50))
    print("Addresses:", get_addresses())
    print("Most expensive:", find_most_expensive())
