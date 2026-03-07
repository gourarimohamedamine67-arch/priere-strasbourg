import requests
from datetime import datetime
import os
import time

# ============================================
# CONFIGURATION
# ============================================
CONTACTS_RAW = os.environ.get("CALLMEBOT_APIKEYS", "").split(",")
CONTACTS = {}
for contact in CONTACTS_RAW:
    if ":" in contact:
        numero, apikey = contact.strip().split(":")
        CONTACTS[numero] = apikey

# ============================================
# INVOCATIONS PAR PRIERE
# ============================================
INVOCATIONS = {
    "Fajr": "🌙 *Fajr* - الفجر\nاللهم إني أسألك علم النافعين\n_Que Allah bénisse votre journée_ 🤲",
    "Dhuhr": "☀️ *Dhuhr* - الظهر\nاللهم صلي على سيدنا محمد\n_Que Allah accepte vos prières_ 🤲",
    "Asr": "🌤️ *Asr* - العصر\nسبحان الله وبحمده\n_Que Allah vous protège_ 🤲",
    "Maghrib": "🌅 *Maghrib* - المغرب\nاللهم إني أسألك الجنة\n_Que Allah illumine vos soirées_ 🤲",
    "Isha": "🌙 *Isha* - العشاء\nأستغفر الله العظيم\n_Que Allah vous accorde une bonne nuit_ 🤲",
}

# ============================================
# RECUPERATION DES HORAIRES - MEINAU STRASBOURG
# ============================================
def get_horaires():
    today = datetime.now()
    # Coordonnées exactes du quartier Meinau Strasbourg
    url = f"https://api.aladhan.com/v1/timings/{today.day}-{today.month}-{today.year}?latitude=48.5539&longitude=7.7455&method=2"
    response = requests.get(url)
    data = response.json()
    timings = data["data"]["timings"]
    return {
        "Fajr": timings["Fajr"],
        "Dhuhr": timings["Dhuhr"],
        "Asr": timings["Asr"],
        "Maghrib": timings["Maghrib"],
        "Isha": timings["Isha"],
    }

# ============================================
# ENVOI WHATSAPP VIA CALLMEBOT
# ============================================
def envoyer_message(priere, heure):
    message = f"🕌 Heure de la prière *{priere}* - {heure}\n\n{INVOCATIONS[priere]}"
    for numero, apikey in CONTACTS.items():
        url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={requests.utils.quote(message)}&apikey={apikey}"
        requests.get(url)
        time.sleep(5)
        print(f"✅ Envoyé à {numero}")

# ============================================
# MAIN
# ============================================
def main():
    now = datetime.now().strftime("%H:%M")
    horaires = get_horaires()
    print(f"🕐 Heure actuelle : {now}")
    for priere, heure in horaires.items():
        print(f"⏰ {priere} à {heure}")
        if heure == now:
            envoyer_message(priere, heure)
            print(f"✅ Message envoyé pour {priere}")

if __name__ == "__main__":
    main()
