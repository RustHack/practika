"""Пользовательские исключения."""


class PropertyNotFoundError(Exception):
    """Объект недвижимости не найден."""
    pass


class InvalidPropertyDataError(Exception):
    """Некорректные данные объекта."""
    pass
