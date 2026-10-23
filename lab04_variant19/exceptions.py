"""Пользовательские исключения."""


class PropertyNotFoundError(Exception):
    """Объект недвижимости не найден."""


class InvalidPropertyDataError(Exception):
    """Некорректные данные объекта."""
