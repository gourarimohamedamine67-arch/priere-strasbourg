import requests
from datetime import datetime, timezone, timedelta
import os

CONTACTS_RAW = os.environ.get("CALLMEBOT_APIKEYS", "").split(",")
CONTACTS = {}
for contact in CONTACTS_RAW:
    if ":" in contact:
        numero, apikey = contact.strip().split(":")
        CONTACTS[numero] = apikey

def get_horaires():
    france = timezone(timedelta(hours=1))
    today = datetime.now(france)
    url = f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}?latitude=48.5539&longitude=7.7455&method=2"
    response = requests.get(url)
    data = response.json()
    timings = data["data"]["timings"]
    return timings, today

def envoyer_message(message):
    for numero, apikey in CONTACTS.items():
        url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={requests.utils.quote(message)}&apikey={apikey}"
        requests.get(url)
        print(f"✅ Envoyé à {numero}")

def main():
    timings, today = get_horaires()
    jour = today.strftime("%d/%m/%Y")
    
    message = f"""🕌 Horaires de prière - Strasbourg Meinau
📅 {jour}

🌙 Fajr : {timings['Fajr']}
☀️ Dhuhr : {timings['Dhuhr']}
🌤️ Asr : {timings['Asr']}
🌅 Maghrib : {timings['Maghrib']}
🌙 Isha : {timings['Isha']}

اللهم تقبل منا صلاتنا 🤲"""

    envoyer_message(message)

if __name__ == "__main__":
    main()
