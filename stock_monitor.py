import os
import requests
import yfinance as yf
import numpy as np
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
translator = Translator()

def send_telegram_message(message):
    # 한국어 번역
    translated = translator.translate(message, dest='ko').text
    
    # 영어 + 한국어 둘 다 보내기
    combined_message = f"{message}\n\n(번역) {translated}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={"chat_id": CHAT_ID, "text": combined_message})
    print(resp.json())  # 디버깅용

def check_volume_alert(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    avg_volume = np.mean(hist['Volume'])
    latest_volume = hist['Volume'][-1]
    
    if latest_volume > 1.5 * avg_volume:
        message = f"🔔 {ticker} trading volume spike! (Current: {latest_volume}, Average: {avg_volume})"
        send_telegram_message(message)

def main():
    for t in ["MSFT", "NVDA", "GOOG"]:
        check_volume_alert(t)

if __name__ == "__main__":
    main()
