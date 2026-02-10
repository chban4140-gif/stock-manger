import yfinance as yf
import numpy as np
import requests
import os

class StockMonitor:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.stocks = ['MSFT', 'NVDA', 'GOOG']
    
    def get_stock_volume(self, symbol):
        try:
            stock_data = yf.Ticker(symbol)
            volume = stock_data.info.get('volume', 0)
            avg_volume = stock_data.info.get('averageVolume', 1)
            return volume, avg_volume
        except Exception as e:
            print(f'Error getting volume for {symbol}: {e}')
            return 0, 1
    
    def send_telegram_message(self, message):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        data = {'chat_id': self.chat_id, 'text': message}
        try:
            requests.post(url, data=data)
            print(f'Message sent: {message}')
        except Exception as e:
            print(f'Error sending message: {e}')
    
    def monitor(self):
        for stock in self.stocks:
            volume, avg_volume = self.get_stock_volume(stock)
            if volume > avg_volume * 1.5:
                message = f'🚨 {stock}: Volume surge detected!\nCurrent: {volume:,.0f}\nAverage: {avg_volume:,.0f}'
                self.send_telegram_message(message)
                print(f'{stock} alert sent!')

if __name__ == '__main__':
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    if bot_token and chat_id:
        monitor = StockMonitor(bot_token, chat_id)
        monitor.monitor()
    else:
        print('BOT_TOKEN or CHAT_ID not set!')
