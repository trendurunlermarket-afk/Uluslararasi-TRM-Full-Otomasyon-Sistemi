# ============================================
# TAM OTOMATİK SOSYAL MEDYA BOTU
# 409 HATASINA KARŞI DAYANIKLI VERSİYON
# ============================================

import os
import time
import random
import schedule
import requests
import threading
import json
from datetime import datetime
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

load_dotenv()

# ============================================
# CLAUDE AI (DOĞRUDAN API)
# ============================================
class ClaudeAI:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY', '')
        self.api_url = "https://api.anthropic.com/v1/messages"
        
    def cevap_uret(self, mesaj):
        if not self.api_key:
            return "Claude API anahtarı bulunamadı."
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-sonnet-20241022",
            "max_tokens": 200,
            "messages": [
                {"role": "user", "content": f"Sen Trend Ürünler Market'in asistanısın. Müşteri sorusu: {mesaj}\n\nKısa, samimi, yardımsever cevap ver."}
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                return response.json()['content'][0]['text']
            return "Üzgünüm, şu anda cevap veremiyorum."
        except:
            return "Üzgünüm, şu anda cevap veremiyorum."


# ============================================
# TELEGRAM BOT
# ============================================
class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.admin_id = '1450144293'
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def mesaj_gonder(self, chat_id, mesaj):
        try:
            url = f"{self.base_url}/sendMessage"
            data = {'chat_id': chat_id, 'text': mesaj, 'parse_mode': 'HTML'}
            response = requests.post(url, data=data)
            return response.status_code == 200
        except:
            return False


# ============================================
# TELEGRAM DİNLEYİCİ (409 HATASINA DAYANIKLI)
# ============================================
def telegram_dinleyici():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN bulunamadı!")
        return
    
    while True:
        try:
            print("🤖 Telegram dinleyici başlatılıyor...")
            bot = telebot.TeleBot(TOKEN)
            claude = ClaudeAI()
            
            @bot.message_handler(commands=['start'])
            def start(message):
                bot.reply_to(message, """
🚀 TRM SİSTEMİ ÇALIŞIYOR!

Komutlar:
/instagram - Instagram paylaşımı
/facebook - Facebook paylaşımı
/tiktok - TikTok paylaşımı
/durum - Sistem durumu

🤖 AI Asistan aktif!
                """)
            
            @bot.message_handler(func=lambda m: True)
            def ai_cevapla(message):
                print(f"🤔 AI soru: {message.text[:30]}...")
                cevap = claude.cevap_uret(message.text)
                bot.reply_to(message, cevap)
            
            # Sonsuz döngüde polling yap
            bot.infinity_polling()
            
        except Exception as e:
            print(f"❌ Telegram hatası: {e}")
            print("🔄 5 saniye sonra yeniden başlatılıyor...")
            time.sleep(5)
            continue


# ============================================
# BASİT WEB SUNUCUSU (Render için)
# ============================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"TRM Bot is running!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()


# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    # Telegram dinleyicisini ayrı thread'de başlat
    threading.Thread(target=telegram_dinleyici, daemon=True).start()
    
    print("✅ Sistem başlatıldı, 409 hatasına karşı dayanıklı!")
    
    # Sonsuz döngü (ana programı canlı tut)
    while True:
        time.sleep(60)
