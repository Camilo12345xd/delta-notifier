import requests
import re
import os
from datetime import datetime

URL = "https://delta.filenetwork.vip/android.html"
TELEGRAM_TOKEN = os.getenv("AAFqOC62p7orgfSNIOAgTD0MoMKMY9MsJgo")
CHAT_ID = os.getenv("9044383382")
VERSION_FILE = "last_version.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_latest_version():
    try:
        r = requests.get(URL, headers=headers, timeout=20)
        content = r.text
        matches = re.findall(r'Delta-(\d+\.\d+\.\d+(?:-\d+)?)\.apk', content, re.IGNORECASE)
        if matches:
            return sorted(set(matches), reverse=True)[0]
        return None
    except Exception as e:
        print(f"Error obteniendo versión: {e}")
        return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{AAFqOC62p7orgfSNIOAgTD0MoMKMY9MsJgo}/sendMessage"
    data = {
        "chat_id": 9044383382,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        print("Mensaje enviado" if r.status_code == 200 else f"Error Telegram: {r.text}")
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def main():
    current = get_latest_version()
    if not current:
        print("No se pudo obtener la versión")
        return

    last = None
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            last = f.read().strip()

    print(f"Versión actual: {current} | Última conocida: {last}")

    if last is None:
        # Primera vez
        with open(VERSION_FILE, "w") as f:
            f.write(current)
        send_telegram(f"📌 <b>Delta Notifier activado</b>\n\nVersión actual detectada:\n<code>{current}</code>\n\n🔗 <a href='{URL}'>Descargar aquí</a>")
    elif current != last:
        # Nueva versión
        with open(VERSION_FILE, "w") as f:
            f.write(current)
        send_telegram(f"🔥 <b>¡Nueva versión de Delta!</b>\n\nAntes: <code>{last}</code>\nAhora: <code>{current}</code>\n\n🔗 <a href='{URL}'>Descargar aquí</a>\n\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    else:
        print("Sin cambios")

if __name__ == "__main__":
    main()
