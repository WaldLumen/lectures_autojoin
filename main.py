import json
from datetime import date

# Загружаем расписание
with open("schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# Функция для определения номера недели (1 или 2)
def get_week_number():
    current_week = date.today().isocalendar().week
    return 1 if current_week % 2 != 0 else 2  # нечётные недели — 1, чётные — 2

# Функция для получения пар на день с учётом недели
def get_day_schedule(day_name):
    week_num = get_week_number()
    day_lessons = schedule.get(day_name, [])

    # Группируем пары по времени
    grouped = {}
    for lesson in day_lessons:
        key = (lesson["start"], lesson["end"])
        grouped.setdefault(key, []).append(lesson)

    # Выбираем первую или вторую запись по неделе
    result = []
    for (start, end), lessons in grouped.items():
        if len(lessons) == 1:
            result.append(lessons[0])
        else:
            index = 0 if week_num == 1 else 1
            if index < len(lessons):
                result.append(lessons[index])
            else:
                result.append(lessons[0])  # на всякий случай fallback

    return result

# Пример использования:
today = "Вівторок"
for lesson in get_day_schedule(today):
    print(f"{lesson['start']}–{lesson['end']}: {lesson['subject']} ({lesson['link']})")

