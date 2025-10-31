import json

import datetime
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions



def browser_actions(link):
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\sylv\Documents")
    options.add_argument(r"--profile-directory=Selenium")

    prefs = {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2
    }
    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    if "meet.google.com" in link :
        # Открываем ссылку
        driver.get(link)
        time.sleep(5)
        driver.find_element("class name", "UywwFc-vQzf8d").click()
    if "us02web.zoom.us" in link:

        driver.get(link)

        driver.find_element("class name", "mbTuDeF1").click()

        driver.find_element("xpath", "//a[contains(text(), 'Join from your browser')]").click()

        time.sleep(3)

        pyautogui.moveTo(2000, 1010, duration=1)
        pyautogui.click()

    return driver





# Функция для определения номера недели (1 или 2)
def get_week_number():
    current_week =datetime.date.today().isocalendar().week
    return 1 if current_week % 2 != 0 else 2  # нечётные недели — 1, чётные — 2

# Функция для получения пар на день с учётом недели
def get_day_schedule(day_num):
    week_num = get_week_number()
    day_lessons = schedule.get(day_num, [])

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
# Загружаем расписание
with open("schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# Пример использования:

is_lecture = False
opened_links = set()

today_lessons = []

while True:
    now = datetime.datetime.now().time()

    if datetime.time(1, 1) <= now <= datetime.time(1, 2) or today_lessons == []:
        today = datetime.date.weekday(datetime.date.today()).__str__()
        today_lessons = get_day_schedule(today)

        # Для справки выводим
        print("Пары на сегодня:")
        for lesson in today_lessons:
            print(f"{lesson['start']}–{lesson['end']}: {lesson['subject']}")

    for lesson in today_lessons:
        start_h, start_m = map(int, lesson["start"].split(":"))
        end_h, end_m = map(int, lesson["end"].split(":"))

        start_time = datetime.time(start_h, start_m)
        end_time = datetime.time(end_h, end_m)

        # Проверяем, что сейчас идёт пара
        if start_time <= now <= end_time:
            # Проверяем, что ссылку ещё не открывали
            if lesson["link"] not in opened_links:
                print(f"Сейчас идёт пара: {lesson['subject']} ({lesson['start']}–{lesson['end']})")
                if not is_lecture:
                    browser = browser_actions(lesson['link'])
                    is_lecture = True

                opened_links.add(lesson["link"])
            is_lecture = False
            break  # если нашли текущую пару, дальше не проверяем

        elif now > end_time and lesson["link"] in opened_links:
            print(f"Пара {lesson['subject']} закончилась ({lesson['end']}). Закрываю браузер.")
            try:
                if browser:
                    browser.quit()
                    browser = None
            except Exception as e:
                print("Ошибка при закрытии браузера:", e)

            opened_links.remove(lesson["link"])


    time.sleep(60)  # проверяем каждую минуту


