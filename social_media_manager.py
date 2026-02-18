# ============================================
# TAM OTOMATİK SOSYAL MEDYA BOTU
# DOĞRUDAN CLAUDE API İSTEKLERİ (kütüphanesiz)
# AI AKTİF VERSİYON
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

load_dotenv()

# ============================================
# CLAUDE AI (DOĞRUDAN API)
# ============================================
class ClaudeAI:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY', '')
        self.api_url = "https://api.anthropic.com/v1/messages"
        
    def cevap_uret(self, mesaj):
        """Doğrudan Claude API'ye istek gönder"""
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
                {"role": "user", "content": f"""
Sen Trend Ürünler Market'in müşteri hizmetleri asistanısın.
Müşteri sorusu: {mesaj}

Kısa, samimi, yardımsever bir cevap ver (maksimum 100 kelime).
Ürün sorulursa fiyat ve özelliklerden bahset.
Satış odaklı ol ama zorlama yapma.
Türkçe cevap ver.
"""}
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                sonuc = response.json()
                return sonuc['content'][0]['text']
            else:
                print(f"❌ Claude API hatası: {response.status_code}")
                return "Üzgünüm, şu anda cevap veremiyorum."
        except Exception as e:
            print(f"❌ Claude bağlantı hatası: {e}")
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
            data = {
                'chat_id': chat_id,
                'text': mesaj,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Telegram mesajı gönderildi")
                return True
            else:
                print(f"❌ Telegram hatası: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram bağlantı hatası: {e}")
            return False
    
    def bildirim_gonder(self, platform, urun_adi, durum):
        mesaj = f"""
🔔 <b>SOSYAL MEDYA BİLDİRİMİ</b>
━━━━━━━━━━━━━━━━━━━━━
📱 Platform: {platform}
📦 Ürün: {urun_adi}
⏱️ Zaman: {datetime.now().strftime('%H:%M')}
📌 Durum: {durum}
━━━━━━━━━━━━━━━━━━━━━
"""
        return self.mesaj_gonder(self.admin_id, mesaj)


# ============================================
# INSTAGRAM BOT (simülasyon)
# ============================================
class InstagramBot:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME', 'trend.urunlermarket')
        self.password = os.getenv('INSTAGRAM_PASSWORD', '')
        
    def giris_yap(self):
        print(f"📱 Instagram: @{self.username} giriş yapılıyor...")
        time.sleep(1)
        print(f"✅ Instagram: @{self.username} giriş başarılı")
        return True
    
    def fotografli_gonderi_paylas(self, resim_url, baslik, urun_linki):
        print(f"📸 Instagram: Gönderi paylaşılıyor...")
        time.sleep(2)
        print(f"✅ Instagram: Gönderi paylaşıldı!")
        return True
    
    def hikaye_paylas(self, resim_url, urun_adi):
        print(f"📱 Instagram: Hikaye paylaşılıyor...")
        time.sleep(1)
        print(f"✅ Instagram: Hikaye paylaşıldı!")
        return True


# ============================================
# FACEBOOK BOT (simülasyon)
# ============================================
class FacebookBot:
    def __init__(self):
        self.page_name = os.getenv('FACEBOOK_PAGE_NAME', 'Trend Urunler Market')
        
    def sayfa_gonderisi_paylas(self, baslik, urun_linki, aciklama):
        print(f"📘 Facebook: Sayfa gönderisi paylaşılıyor...")
        time.sleep(2)
        print(f"✅ Facebook: Gönderi paylaşıldı!")
        return True


# ============================================
# TİKTOK BOT (simülasyon)
# ============================================
class TikTokBot:
    def __init__(self):
        self.username = os.getenv('TIKTOK_USERNAME', '')
        
    def giris_yap(self):
        print(f"🎵 TikTok: @{self.username} giriş yapılıyor...")
        time.sleep(1)
        print(f"✅ TikTok giriş başarılı")
        return True
    
    def paylasim_hazirla(self, urun):
        print(f"🎵 TikTok: Video paylaşılıyor...")
        time.sleep(2)
        print(f"✅ TikTok video paylaşıldı!")
        return True


# ============================================
# ÜRÜN VERİTABANI
# ============================================
class UrunVeritabani:
    def __init__(self):
        self.urunler = [
            {'id': 1, 'ad': 'Xiaomi Akıllı Bileklik', 'fiyat': 449, 
             'link': 'https://www.trendyol.com/...', 
             'aciklama': 'Kalp atışı takibi, adım sayar', 
             'kategori': 'elektronik'},
            {'id': 2, 'ad': 'ChefMax Doğrayıcı', 'fiyat': 449,
             'link': 'https://www.trendyol.com/...',
             'aciklama': '1000W güç, 3.5L cam hazne',
             'kategori': 'mutfak'},
        ]
    
    def rastgele_urun_sec(self):
        return random.choice(self.urunler)


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
    print(f"✅ Web sunucusu {port} portunda başlatıldı.")
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()


# ============================================
# SOSYAL MEDYA YÖNETİCİSİ
# ============================================
class SosyalMedyaYoneticisi:
    def __init__(self):
        print("🚀 TRM OTOMASYON BAŞLATILIYOR...")
        
        self.claude = ClaudeAI()
        self.telegram = TelegramBot()
        self.instagram = InstagramBot()
        self.facebook = FacebookBot()
        self.tiktok = TikTokBot()
        self.urunler = UrunVeritabani()
        
        self.paylasim_sayaci = {'instagram': 0, 'facebook': 0, 'tiktok': 0}
        
        print(f"🤖 Claude AI: {'✅ Aktif' if self.claude.api_key else '❌ Devre dışı'}")
        self.instagram.giris_yap()
    
    def telegram_rapor(self):
        toplam = sum(self.paylasim_sayaci.values())
        rapor = f"""
📊 SAATLİK RAPOR
📱 Instagram: {self.paylasim_sayaci['instagram']}
📘 Facebook: {self.paylasim_sayaci['facebook']}
🎵 TikTok: {self.paylasim_sayaci['tiktok']}
🎯 Toplam: {toplam}
        """
        self.telegram.mesaj_gonder('1450144293', rapor)
    
    def calistir(self):
        schedule.every().hour.at(":05").do(self.telegram_rapor)
        while True:
            schedule.run_pending()
            time.sleep(60)


# ============================================
# TELEGRAM KOMUTLARI
# ============================================
def telegram_dinleyici():
    import telebot
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    bot = telebot.TeleBot(TOKEN)
    yonetici = SosyalMedyaYoneticisi()
    
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
        cevap = yonetici.claude.cevap_uret(message.text)
        bot.reply_to(message, cevap)
    
    bot.infinity_polling()


# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    threading.Thread(target=telegram_dinleyici, daemon=True).start()
    yonetici = SosyalMedyaYoneticisi()
    yonetici.calistir()
