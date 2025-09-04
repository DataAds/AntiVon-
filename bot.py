import requests
import time
import os
from datetime import datetime, timedelta

LAT, LON = 43.65, 51.15
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# перевод градусов в русские названия ветра
def deg_to_dir_ru(deg):
    if deg >= 337.5 or deg < 22.5:
        return "Северный"
    elif 22.5 <= deg < 67.5:
        return "Северо-Восточный"
    elif 67.5 <= deg < 112.5:
        return "Восточный"
    elif 112.5 <= deg < 157.5:
        return "Юго-Восточный"
    elif 157.5 <= deg < 202.5:
        return "Южный"
    elif 202.5 <= deg < 247.5:
        return "Юго-Западный"
    elif 247.5 <= deg < 292.5:
        return "Западный"
    else:
        return "Северо-Западный"

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    r = requests.get(url).json()
    wind_speed = r["current_weather"]["windspeed"]
    wind_deg = r["current_weather"]["winddirection"]
    wind_dir = deg_to_dir_ru(wind_deg)
    return wind_speed, wind_dir

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

last_daily_report = None
last_wind_check = 0

while True:
    now = datetime.utcnow() + timedelta(hours=3)  # UTC+3 = МСК
    timestamp = time.time()

    # ----- 1. Ежедневный отчёт (раз в день, начиная с 17:00) -----
    if now.hour >= 17:
        if last_daily_report is None or last_daily_report.date() < now.date():
            wind_speed, wind_dir = get_weather()
            message = f"Привет! Я работаю 🚀\nСейчас в Актау ветер {wind_speed} м/с, направление {wind_dir}"
            send_message(message)
            last_daily_report = now

    # ----- 2. Алярм: проверка каждые 30 мин -----
    if timestamp - last_wind_check >= 1800:  # 1800 сек = 30 минут
        wind_speed, wind_dir = get_weather()
        if wind_dir in ["Северный", "Северо-Западный"]:
            send_message(f"Алярм!!! говноветер {wind_dir}, скорость {wind_speed} м/с")
        last_wind_check = timestamp

    time.sleep(30)  # чтобы не грузить процессор
