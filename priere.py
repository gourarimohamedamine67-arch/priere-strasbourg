import requests
from datetime import datetime
import pywhatkit as kit
import time

# ============================================
# CONFIGURATION - MODIFIE CES VALEURS
# ============================================
NUMEROS_FAMILLE = [
    "+33620009607",  # Remplace par les vrais numéros
    "+33658506214",
]

VILLE = "Strasbourg"
PAYS = "FR"

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
# RECUPERATION DES HORAIRES
# ============================================
def get_horaires():
    today = datetime.now()
    url = f"http://api.aladhan.com/v1/timingsByCity/{today.day}-{today.month}-{today.year}?city={VILLE}&country={PAYS}&method=2"
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
# ENVOI WHATSAPP
# ============================================
def envoyer_message(priere, heure):
    message = f"🕌 Heure de la prière *{priere}* - {heure}\n\n{INVOCATIONS[priere]}"
    for numero in NUMEROS_FAMILLE:
        kit.sendwhatmsg_instantly(numero, message)
        time.sleep(10)

# ============================================
# MAIN
# ============================================
def main():
    now = datetime.now().strftime("%H:%M")
    horaires = get_horaires()
    
    for priere, heure in horaires.items():
        if heure == now:
            envoyer_message(priere, heure)
            print(f"✅ Message envoyé pour {priere}")

if __name__ == "__main__":
    main()
