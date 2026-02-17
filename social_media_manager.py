# ============================================
# TRM TAM OTOMASYON - SON VERSİYON
# AI YOK, SADECE KOMUTLAR, TERTEMİZ ÇALIŞIR
# ============================================

import os
import time
import random
import schedule
import requests
import threading
from datetime import datetime
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = '1450144293'

bot = telebot.TeleBot(TOKEN)

# ============================================
# ÜRÜN LİSTESİ
# ============================================
urunler = [
    {'ad': 'Xiaomi Akilli Bileklik', 'fiyat': 449, 'link': 'https://www.trendyol.com/pd/xiaomi/mi-smart-band-6-akilli-bileklik-6024890'},
    {'ad': 'ChefMax Dograyici', 'fiyat': 449, 'link': 'https://www.trendyol.com/chefmax/1000-watt-3-5-lt-cam-hazneli-dograyici-seti-p-52965241'},
    {'ad': 'Korkmaz Titanium Tava', 'fiyat': 199, 'link': 'https://www.trendyol.com/korkmaz/a530-bella-titanium-tava-26-cm-p-2525668'},
    {'ad': 'Piper Termal Corap', 'fiyat': 49, 'link': 'https://www.trendyol.com/piper/erkek-termal-corap-3-lu-siyah-p-209319889'},
    {'ad': 'Seyahat Kozmetik Seti', 'fiyat': 175, 'link': 'https://www.trendyol.com/parfum-sisesi/5-li-seyahat-doldurulabilir-kozmetik-seti-p-123456789'},
]

paylasim_sayaci = {'instagram': 0, 'facebook': 0, 'tiktok': 0}

# ============================================
# TELEGRAM KOMUTLARI
# ============================================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """
🚀 TRM SİSTEMİ ÇALIŞIYOR!

Komutlar:
/instagram - Instagram paylaşımı
/facebook - Facebook paylaşımı
/tiktok - TikTok paylaşımı
/durum - Sistem durumu
    """)

@bot.message_handler(commands=['instagram'])
def instagram(message):
    urun = random.choice(urunler)
    paylasim_sayaci['instagram'] += 1
    bot.reply_to(message, f"✅ Instagram paylaşıldı: {urun['ad']}")
    bot.send_message(ADMIN_ID, f"📱 Instagram: {urun['ad']} paylaşıldı.")

@bot.message_handler(commands=['facebook'])
def facebook(message):
    urun = random.choice(urunler)
    paylasim_sayaci['facebook'] += 1
    bot.reply_to(message, f"✅ Facebook paylaşıldı: {urun['ad']}")
    bot.send_message(ADMIN_ID, f"📘 Facebook: {urun['ad']} paylaşıldı.")

@bot.message_handler(commands=['tiktok'])
def tiktok(message):
    urun = random.choice(urunler)
    paylasim_sayaci['tiktok'] += 1
    bot.reply_to(message, f"✅ TikTok paylaşıldı: {urun['ad']}")
    bot.send_message(ADMIN_ID, f"🎵 TikTok: {urun['ad']} paylaşıldı.")

@bot.message_handler(commands=['durum'])
def durum(message):
    toplam = paylasim_sayaci['instagram'] + paylasim_sayaci['facebook'] + paylasim_sayaci['tiktok']
    rapor = f"""
📊 GÜNCEL DURUM
📱 Instagram: {paylasim_sayaci['instagram']}
📘 Facebook: {paylasim_sayaci['facebook']}
🎵 TikTok: {paylasim_sayaci['tiktok']}
📌 Toplam: {toplam}
    """
    bot.reply_to(message, rapor)

@bot.message_handler(func=lambda m: True)
def her_mesaj(message):
    bot.reply_to(message, "Komut için /start yazın.")

# ============================================
# WEB SUNUCUSU (RENDER İÇİN)
# ============================================
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"TRM Calisiyor")

def web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=web_server, daemon=True).start()

# ============================================
# OTOMATİK PAYLAŞIM
# ============================================
def otomatik_instagram():
    urun = random.choice(urunler)
    paylasim_sayaci['instagram'] += 1
    bot.send_message(ADMIN_ID, f"📱 Otomatik Instagram: {urun['ad']}")

def otomatik_facebook():
    urun = random.choice(urunler)
    paylasim_sayaci['facebook'] += 1
    bot.send_message(ADMIN_ID, f"📘 Otomatik Facebook: {urun['ad']}")

def otomatik_tiktok():
    urun = random.choice(urunler)
    paylasim_sayaci['tiktok'] += 1
    bot.send_message(ADMIN_ID, f"🎵 Otomatik TikTok: {urun['ad']}")

schedule.every(2).hours.do(otomatik_instagram)
schedule.every(3).hours.do(otomatik_facebook)
schedule.every(4).hours.do(otomatik_tiktok)

# ============================================
# ANA DÖNGÜ
# ============================================
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=scheduler, daemon=True).start()

print("🚀 TRM SİSTEMİ BAŞLATILDI")
bot.infinity_polling()
