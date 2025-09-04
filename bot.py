import requests
import time
import os

LAT, LON = 43.65, 51.15
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# перевод градусов в стороны света
def deg_to_dir(deg):
    dirs = ['N','NE','E','SE','S','SW','W','NW']
    ix = round(deg / 45) % 8
    return dirs[ix]

def get_wind():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    r = requests.get(url).json()
    wind_deg = r["current_weather"]["winddirection"]
    wind_dir = deg_to_dir(wind_deg)
    return wind_dir

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

while True:
    wind = get_wind()
    if wind in ["NW", "N"]:  # северо-запад или север
        send_message(f"⚡ В Актау ветер {wind}")
    time.sleep(600)  # проверка каждые 10 минут
