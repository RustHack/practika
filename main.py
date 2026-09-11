def flight_duration(dep, arr):
    """Вычисляет продолжительность рейса в минутах.
    Если arr < dep — рейс через полночь.
    """
    if arr >= dep:
        return arr - dep
    else:
        return (24 * 60 - dep) + arr   # 1440 - dep + arr


def main():
    print("Анализ продолжительности авиарейсов")
    print("Время вводится в минутах от начала суток (0–1439)\n")

    # Ввод количества рейсов
    while True:
        try:
            n = int(input("Введите количество рейсов: "))
            if n > 0:
                break
            print("Количество рейсов должно быть положительным.")
        except ValueError:
            print("Ошибка: введите целое число.")

    durations = []   # список продолжительностей

    # Ввод данных по каждому рейсу
    for i in range(1, n + 1):
        print(f"\nРейс {i}:")
        while True:
            try:
                dep = int(input("  Время отправления (мин): "))
                arr = int(input("  Время прибытия (мин): "))
                if 0 <= dep < 1440 and 0 <= arr < 1440:
                    break
                print("  Время должно быть в диапазоне 0–1439.")
            except ValueError:
                print("  Ошибка: введите целые числа.")

        dur = flight_duration(dep, arr)
        durations.append(dur)
        print(f"  Продолжительность рейса: {dur} мин ({dur // 60} ч {dur % 60} мин)")

    # Основные расчёты
    max_dur = max(durations)
    min_dur = min(durations)
    avg_dur = sum(durations) / len(durations)

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 50)
    print(f"Самый продолжительный рейс: {max_dur} мин ({max_dur // 60} ч {max_dur % 60} мин)")
    print(f"Самый короткий рейс:       {min_dur} мин ({min_dur // 60} ч {min_dur % 60} мин)")
    print(f"Средняя продолжительность: {avg_dur:.1f} мин ({avg_dur / 60:.1f} ч)")

    # Количество рейсов дольше заданного значения
    while True:
        try:
            threshold = int(input("\nВведите пороговое значение (мин): "))
            if threshold >= 0:
                break
            print("Порог не может быть отрицательным.")
        except ValueError:
            print("Ошибка: введите целое число.")

    count = sum(1 for d in durations if d > threshold)
    print(f"Количество рейсов продолжительностью более {threshold} мин: {count}")


if __name__ == "__main__":
    main()