import requests
import time
import os

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

def get_wind():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    r = requests.get(url).json()
    wind_deg = r["current_weather"]["winddirection"]
    wind_dir = deg_to_dir_ru(wind_deg)
    return wind_dir

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

while True:
    wind = get_wind()
    if wind in ["Северный", "Северо-Западный"]:
        send_message(f"Алярм!!! говноветер {wind}")
    time.sleep(600)  # проверка каждые 10 минут
