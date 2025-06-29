import requests
import time

BOT_TOKEN = "7801946514:AAGVMfs8IuhoJMX2hn6bRQF-GmUX9Bu9eag"
CHAT_ID = "922896992"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_prices():
    print("🔄 بدأ الفحص كل دقيقة (Threshold = -30%)")
    url = "https://api.gate.io/api/v4/spot/tickers"
    response = requests.get(url).json()
    for coin in response:
        if not coin["currency_pair"].endswith("_usdt"):
            continue
        if any(x in coin["currency_pair"] for x in ["3S", "3L", "5S", "5L"]):
            continue  # استبعاد ETF
        change = float(coin["change_percentage"])
        if change <= -30:
            send_alert(f"⚠️ {coin['currency_pair']} هبط {change}% خلال 24 ساعة")

while True:
    check_prices()
    time.sleep(60)
