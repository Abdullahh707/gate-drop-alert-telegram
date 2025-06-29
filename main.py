import requests
import time

BOT_TOKEN = "7801946514:AAGVMfs8IuhoJMX2hn6bRQF-GmUX9Bu9eag"
CHAT_ID = "922896992"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def check_prices():
    print("🔄 بدأ الفحص كل دقيقة (Threshold = -30%)")
    url = "https://api.gate.io/api/v4/spot/tickers"
    try:
        response = requests.get(url, verify=False).json()  # ✅ تجاوز شهادة SSL
    except Exception as e:
        print("❌ فشل الاتصال:", e)
        return

    for coin in response:
        if not coin["currency_pair"].endswith("_usdt"):
            continue
        if "3S" in coin["currency_pair"] or "3L" in coin["currency_pair"] or \
           "5S" in coin["currency_pair"] or "5L" in coin["currency_pair"]:
            continue  # استثناء ETF

        change = float(coin["change_percentage"])
        if change >= 0:
:
            send_alert(f"⚠️ {coin['currency_pair']} هبط {change}% خلال 24 ساعة")

while True:
    check_prices()
    time.sleep(60)
