class Project:
    def __init__(self, name, manager, participants, budget, status):
        self.name = name
        self.manager = manager
        self.participants = participants
        self.budget = budget
        self.status = status

    def __str__(self):
        return (f"«{self.name}» | Руководитель: {self.manager} | "
                f"Участников: {self.participants} | "
                f"Бюджет: {self.budget:,.0f} | Статус: {self.status}")


def print_projects(projects, title="Список проектов"):
    print(f"\n{title}")
    print("-" * 80)
    if not projects:
        print("  (пусто)")
        return
    for i, p in enumerate(projects, 1):
        print(f"{i}. {p}")


def search_by_manager(projects, manager):
    """Поиск проектов по руководителю (без учёта регистра)"""
    manager_lower = manager.lower()
    return [p for p in projects if p.manager.lower() == manager_lower]


def filter_by_budget(projects, min_budget=None, max_budget=None):
    """Фильтрация по бюджету"""
    result = projects
    if min_budget is not None:
        result = [p for p in result if p.budget >= min_budget]
    if max_budget is not None:
        result = [p for p in result if p.budget <= max_budget]
    return result


def average_budget(projects):
    """Средний бюджет"""
    if not projects:
        return 0.0
    return sum(p.budget for p in projects) / len(projects)


def most_expensive(projects):
    """Самый дорогой проект"""
    if not projects:
        return None
    return max(projects, key=lambda p: p.budget)


def unique_statuses(projects):
    """Список уникальных статусов"""
    return sorted(set(p.status for p in projects))


def sort_by_budget(projects, reverse=False):
    """Сортировка по бюджету (по возрастанию / убыванию)"""
    return sorted(projects, key=lambda p: p.budget, reverse=reverse)


def main():
    # ---------- Пример данных ----------
    projects = [
        Project("Мобильное приложение", "Иванов А.С.", 8, 2_500_000, "В работе"),
        Project("Веб-портал", "Петрова М.И.", 12, 4_200_000, "Завершён"),
        Project("CRM-система", "Иванов А.С.", 15, 6_800_000, "В работе"),
        Project("Аналитика данных", "Сидоров К.В.", 6, 1_900_000, "Планирование"),
        Project("Мобильное приложение 2.0", "Петрова М.И.", 10, 3_100_000, "В работе"),
        Project("ИИ-ассистент", "Козлова Е.Н.", 9, 5_500_000, "Тестирование"),
        Project("Интернет-магазин", "Сидоров К.В.", 7, 2_200_000, "Завершён"),
    ]

    print("=" * 80)
    print("СИСТЕМА УПРАВЛЕНИЯ ПРОЕКТАМИ")
    print("=" * 80)

    print_projects(projects, "Все проекты")

    # 1. Поиск по руководителю
    manager = "Иванов А.С."
    found = search_by_manager(projects, manager)
    print_projects(found, f"Проекты руководителя «{manager}»")

    # 2. Фильтрация по бюджету
    filtered = filter_by_budget(projects, min_budget=3_000_000, max_budget=6_000_000)
    print_projects(filtered, "Проекты с бюджетом от 3 000 000 до 6 000 000")

    # 3. Средний бюджет
    avg = average_budget(projects)
    print(f"\nСредний бюджет всех проектов: {avg:,.0f}")

    # 4. Самый дорогой проект
    expensive = most_expensive(projects)
    print(f"\nСамый дорогой проект:\n  {expensive}")

    # 5. Список статусов
    statuses = unique_statuses(projects)
    print(f"\nСписок статусов: {', '.join(statuses)}")

    # 6. Сортировка по бюджету
    sorted_asc = sort_by_budget(projects)
    print_projects(sorted_asc, "Проекты, отсортированные по бюджету (по возрастанию)")

    sorted_desc = sort_by_budget(projects, reverse=True)
    print_projects(sorted_desc, "Проекты, отсортированные по бюджету (по убыванию)")


if __name__ == "__main__":
    main()