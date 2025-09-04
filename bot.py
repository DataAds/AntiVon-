import requests
import time
import os

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
LAT, LON = 43.65, 51.15
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_wind():
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={LAT}&lon={LON}&extra=true"
    headers = {"X-Yandex-API-Key": YANDEX_API_KEY}
    r = requests.get(url, headers=headers).json()
    return r["fact"]["wind_dir"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

while True:
    wind = get_wind()
    if wind == "nw":  # северо-запад
        send_message(f"⚡ В Актау ветер северо-запад ({wind})")
    time.sleep(600)  # 10 минут
