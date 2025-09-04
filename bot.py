import requests
import time
import os
import threading
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

LAT, LON = 43.65, 51.15
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

def bot_loop():
    last_daily_report = None
    last_wind_check = 0

    while True:
        now = datetime.utcnow() + timedelta(hours=3)  # МСК
        ts = time.time()

        # Ежедневный отчёт
        if now.hour >= 17:
            if last_daily_report is None or last_daily_report.date() < now.date():
                ws, wd = get_weather()
                send_message(f"Привет! Я работаю 🚀\nСейчас в Актау ветер {ws} м/с, направление {wd}")
                last_daily_report = now

        # Алярм раз в 30 мин
        if ts - last_wind_check >= 1800:
            ws, wd = get_weather()
            if wd in ["Северный", "Северо-Западный"]:
                send_message(f"Алярм!!! говноветер {wd}, скорость {ws} м/с")
            last_wind_check = ts

        time.sleep(30)

# 🔹 Минимальный HTTP-сервер, чтобы Render не ругался
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    t = threading.Thread(target=bot_loop, daemon=True)
    t.start()

    # Запускаем HTTP-сервер (Render требует открыть порт)
    port = int(os.environ.get("PORT", 5000))
    server = HTTPServer(("", port), Handler)
    server.serve_forever()

