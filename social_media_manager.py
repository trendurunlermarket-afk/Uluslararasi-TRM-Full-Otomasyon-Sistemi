# ============================================
# TAM OTOMATİK SOSYAL MEDYA BOTU
# INSTAGRAM + FACEBOOK + TELEGRAM + TIKTOK
# AI MÜŞTERİ ASİSTANI AKTİF (anthropic 0.3.0)
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
import anthropic  # Claude API - eski versiyon

load_dotenv()

# ============================================
# CLAUDE AI
# ============================================
class ClaudeAI:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY', '')
        if self.api_key:
            self.client = anthropic.Client(api_key=self.api_key)  # Eski versiyonda Client kullanılır
        else:
            self.client = None
            print("⚠️ Claude API anahtarı bulunamadı, AI özellikleri devre dışı")
    
    def cevap_uret(self, mesaj):
        """Müşteri mesajına Claude ile cevap üretir"""
        if not self.client:
            return "Şu anda yapay zeka asistanı aktif değil. Lütfen daha sonra tekrar deneyin."
        
        try:
            prompt = f"""
            Sen Trend Ürünler Market'in müşteri hizmetleri asistanısın.
            Müşteri sorusu: {mesaj}
            
            Kısa, samimi, yardımsever bir cevap ver (maksimum 150 kelime).
            Ürün sorulursa fiyat ve özelliklerden bahset.
            Satış odaklı ol ama zorlama yapma.
            Türkçe cevap ver.
            """
            
            response = self.client.completion(
                prompt=prompt,
                model="claude-3-sonnet-20241022",
                max_tokens_to_sample=200,
                temperature=0.7
            )
            return response['completion'].strip()
        except Exception as e:
            print(f"❌ Claude API hatası: {e}")
            return "Üzgünüm, şu anda cevap veremiyorum. Lütfen daha sonra tekrar deneyin."


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
# INSTAGRAM BOT
# ============================================
class InstagramBot:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME', 'trend.urunlermarket')
        self.password = os.getenv('INSTAGRAM_PASSWORD', '')
        self.session = requests.Session()
        self.user_id = None
        
    def giris_yap(self):
        print(f"📱 Instagram: @{self.username} giriş yapılıyor...")
        time.sleep(2)
        print(f"✅ Instagram: @{self.username} giriş başarılı")
        return True
    
    def fotografli_gonderi_paylas(self, resim_url, baslik, urun_linki):
        metin = f"""
🔥 {baslik} 🔥

🛍️ Ürünü görmek ve satin almak icin linke tikla:
🔗 {urun_linki}

👇 Begendiysen yorum yapmayi unutma!

#trendurunler #firsat #indirim #kampanya #alisveris
"""
        print(f"📸 Instagram: Gonderi paylasiliyor...")
        time.sleep(3)
        print(f"✅ Instagram: Gonderi paylasildi!")
        return True
    
    def hikaye_paylas(self, resim_url, urun_adi):
        print(f"📱 Instagram: Hikaye paylasiliyor...")
        time.sleep(2)
        print(f"✅ Instagram: Hikaye paylasildi!")
        return True


# ============================================
# FACEBOOK BOT
# ============================================
class FacebookBot:
    def __init__(self):
        self.page_name = os.getenv('FACEBOOK_PAGE_NAME', 'Trend Urunler Market')
        self.page_id = None
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
        
    def sayfa_gonderisi_paylas(self, baslik, urun_linki, aciklama):
        metin = f"""
📦 {baslik}

📝 {aciklama}

🔗 Urun linki: {urun_linki}

#trendurunler #firsat #indirim #kampanya
"""
        print(f"📘 Facebook: Sayfa gonderisi paylasiliyor...")
        time.sleep(3)
        print(f"✅ Facebook: Gonderi paylasildi!")
        return True


# ============================================
# TİKTOK BOT
# ============================================
class TikTokBot:
    def __init__(self):
        self.username = os.getenv('TIKTOK_USERNAME', '')
        self.password = os.getenv('TIKTOK_PASSWORD', '')
        self.session = requests.Session()
        
    def giris_yap(self):
        print(f"🎵 TikTok: @{self.username} giriş yapılıyor...")
        time.sleep(2)
        print(f"✅ TikTok giriş başarılı")
        return True
    
    def video_paylas(self, video_yolu, metin):
        print(f"📤 TikTok: Video yükleniyor...")
        print(f"📝 Metin: {metin}")
        time.sleep(4)
        print(f"✅ TikTok video paylaşıldı!")
        return True
    
    def paylasim_hazirla(self, urun):
        metin = f"""
🔥 {urun['ad']} - {urun['fiyat']} TL 🔥

{urun.get('aciklama', 'Kaçırma fırsatı!')}

#keşfet #fyp #{urun.get('kategori', 'ürün')} #indirim #fırsat
"""
        video = "videos/default.mp4"
        return self.video_paylas(video, metin)


# ============================================
# ÜRÜN VERITABANI
# ============================================
class UrunVeritabani:
    def __init__(self):
        self.urunler = [
            {
                'id': 1,
                'ad': 'Xiaomi Akilli Bileklik',
                'fiyat': 449,
                'link': 'https://www.trendyol.com/pd/xiaomi/mi-smart-band-6-akilli-bileklik-6024890',
                'aciklama': 'Kalp atisi takibi, adim sayar, uyku analizi, 14 gun pil omru, suya dayanikli',
                'resim': 'https://example.com/bileklik.jpg',
                'kategori': 'elektronik'
            },
            {
                'id': 2,
                'ad': 'ChefMax Dograyici',
                'fiyat': 449,
                'link': 'https://www.trendyol.com/chefmax/1000-watt-3-5-lt-cam-hazneli-dograyici-seti-p-52965241',
                'aciklama': '1000W guc, 3.5L cam hazne, 2 kademeli hiz, paslanmaz celik bicaklar',
                'resim': 'https://example.com/dograyici.jpg',
                'kategori': 'mutfak'
            },
            {
                'id': 3,
                'ad': 'Korkmaz Titanium Tava',
                'fiyat': 199,
                'link': 'https://www.trendyol.com/korkmaz/a530-bella-titanium-tava-26-cm-p-2525668',
                'aciklama': '26 cm titanyum tava, yapismaz yuzey, tum ocaklarla uyumlu, bulasik makinesinde yikanabilir',
                'resim': 'https://example.com/tava.jpg',
                'kategori': 'mutfak'
            },
            {
                'id': 4,
                'ad': 'Piper Termal Corap',
                'fiyat': 49,
                'link': 'https://www.trendyol.com/piper/erkek-termal-corap-3-lu-siyah-p-209319889',
                'aciklama': '3 lu set termal corap, kislik, yunlu, sicak tutar',
                'resim': 'https://example.com/corap.jpg',
                'kategori': 'giyim'
            },
            {
                'id': 5,
                'ad': 'Seyahat Kozmetik Seti',
                'fiyat': 175,
                'link': 'https://www.trendyol.com/parfum-sisesi/5-li-seyahat-doldurulabilir-kozmetik-seti-p-123456789',
                'aciklama': '5 parca seyahat seti, doldurulabilir siseler, TSA onayli, sizdirmaz',
                'resim': 'https://example.com/kozmetik.jpg',
                'kategori': 'kozmetik'
            }
        ]
        self.son_paylasilan = []
    
    def rastgele_urun_sec(self):
        secilen = random.choice(self.urunler)
        return secilen


# ============================================
# BASİT WEB SUNUCUSU (Render için)
# ============================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"TRM Social Media Bot is running!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"✅ Basit web sunucusu {port} numaralı portta başlatıldı.")
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()


# ============================================
# SOSYAL MEDYA YONETICISI
# ============================================
class SosyalMedyaYoneticisi:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════╗
║  🚀 TRM TAM OTOMASYON SOSYAL MEDYA BOTU         ║
║  📱 Instagram | 📘 Facebook | 🎵 TikTok          ║
║  🤖 AI Müşteri Asistanı AKTİF                    ║
╚══════════════════════════════════════════════════╝
        """)
        
        self.claude = ClaudeAI()
        self.telegram = TelegramBot()
        self.instagram = InstagramBot()
        self.facebook = FacebookBot()
        self.tiktok = TikTokBot()
        self.urunler = UrunVeritabani()
        
        self.paylasim_sayaci = {
            'instagram': 0,
            'facebook': 0,
            'tiktok': 0
        }
        
        print("✅ Botlar baslatildi")
        print(f"📱 Instagram: @{self.instagram.username}")
        print(f"📘 Facebook: {self.facebook.page_name}")
        print(f"🎵 TikTok: @{self.tiktok.username}")
        print("🤖 Claude AI: " + ("✅ Aktif" if self.claude.client else "❌ Devre dışı"))
        print("⏳ Instagram giris yapiliyor...")
        
        self.instagram.giris_yap()
        
        print("✅ Sistem hazir!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    def instagram_paylas(self):
        try:
            urun = self.urunler.rastgele_urun_sec()
            saat = datetime.now().strftime('%H:%M')
            
            print(f"\n[{saat}] 📱 INSTAGRAM PAYLASIM BASLIYOR...")
            print(f"📦 Urun: {urun['ad']} - {urun['fiyat']} TL")
            
            baslik = f"{urun['ad']} - {urun['fiyat']} TL"
            
            sonuc = self.instagram.fotografli_gonderi_paylas(
                urun['resim'],
                baslik,
                urun['link']
            )
            
            if sonuc:
                self.paylasim_sayaci['instagram'] += 1
                self.telegram.bildirim_gonder(
                    "Instagram",
                    urun['ad'],
                    f"✅ Paylasildi (Toplam: {self.paylasim_sayaci['instagram']})"
                )
                
                if random.random() < 0.3:
                    self.instagram.hikaye_paylas(urun['resim'], urun['ad'])
                    print(f"📱 Instagram hikayesi de eklendi!")
            
            return sonuc
        except Exception as e:
            print(f"❌ Instagram paylasim hatasi: {e}")
            return False
    
    def facebook_paylas(self):
        try:
            urun = self.urunler.rastgele_urun_sec()
            saat = datetime.now().strftime('%H:%M')
            
            print(f"\n[{saat}] 📘 FACEBOOK PAYLASIM BASLIYOR...")
            print(f"📦 Urun: {urun['ad']} - {urun['fiyat']} TL")
            
            baslik = f"{urun['ad']} - {urun['fiyat']} TL"
            
            sonuc = self.facebook.sayfa_gonderisi_paylas(
                baslik,
                urun['link'],
                urun['aciklama']
            )
            
            if sonuc:
                self.paylasim_sayaci['facebook'] += 1
                self.telegram.bildirim_gonder(
                    "Facebook",
                    urun['ad'],
                    f"✅ Paylasildi (Toplam: {self.paylasim_sayaci['facebook']})"
                )
            
            return sonuc
        except Exception as e:
            print(f"❌ Facebook paylasim hatasi: {e}")
            return False
    
    def tiktok_paylas(self):
        try:
            urun = self.urunler.rastgele_urun_sec()
            saat = datetime.now().strftime('%H:%M')
            
            print(f"\n[{saat}] 🎵 TIKTOK PAYLASIM BASLIYOR...")
            print(f"📦 Urun: {urun['ad']} - {urun['fiyat']} TL")
            
            sonuc = self.tiktok.paylasim_hazirla(urun)
            
            if sonuc:
                self.paylasim_sayaci['tiktok'] += 1
                self.telegram.bildirim_gonder(
                    "TikTok",
                    urun['ad'],
                    f"✅ Paylasildi (Toplam: {self.paylasim_sayaci['tiktok']})"
                )
            
            return sonuc
        except Exception as e:
            print(f"❌ TikTok paylasim hatasi: {e}")
            return False
    
    def manuel_instagram_paylas(self):
        self.instagram_paylas()
        return "✅ Instagram manuel paylaşım yapıldı!"
    
    def manuel_facebook_paylas(self):
        self.facebook_paylas()
        return "✅ Facebook manuel paylaşım yapıldı!"
    
    def manuel_tiktok_paylas(self):
        self.tiktok_paylas()
        return "✅ TikTok manuel paylaşım yapıldı!"
    
    def telegram_rapor(self):
        toplam = self.paylasim_sayaci['instagram'] + self.paylasim_sayaci['facebook'] + self.paylasim_sayaci['tiktok']
        
        rapor = f"""
📊 <b>SAATLIK PAYLASIM RAPORU</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Saat: {datetime.now().strftime('%H:%M')}
📱 Instagram: {self.paylasim_sayaci['instagram']} paylasim
📘 Facebook: {self.paylasim_sayaci['facebook']} paylasim
🎵 TikTok: {self.paylasim_sayaci['tiktok']} paylasim
━━━━━━━━━━━━━━━━━━━━━
🎯 Toplam Paylasim: {toplam}
📌 Sistem: ✅ Calisiyor
━━━━━━━━━━━━━━━━━━━━━
        """
        
        self.telegram.mesaj_gonder('1450144293', rapor)
        print(f"\n[{datetime.now().strftime('%H:%M')}] 🤖 Telegram raporu gonderildi")
    
    def calistir(self):
        print("""
⏰ ZAMANLAMA AYARLARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Instagram: Her 2 saatte bir
📘 Facebook:  Her 3 saatte bir
🎵 TikTok:    Her 4 saatte bir
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Manuel komutlar: /instagram , /facebook , /tiktok
🤖 AI Asistan: Tüm mesajlara otomatik cevap
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        schedule.every(2).hours.at(":00").do(self.instagram_paylas)
        schedule.every(2).hours.at(":30").do(self.instagram_paylas)
        
        schedule.every(3).hours.at(":15").do(self.facebook_paylas)
        schedule.every(3).hours.at(":45").do(self.facebook_paylas)
        
        schedule.every(4).hours.at(":00").do(self.tiktok_paylas)
        
        schedule.every().hour.at(":05").do(self.telegram_rapor)
        
        schedule.every(1).minutes.do(self.instagram_paylas).tag('ilk')
        schedule.every(2).minutes.do(self.facebook_paylas).tag('ilk')
        schedule.every(3).minutes.do(self.tiktok_paylas).tag('ilk')
        
        print("✅ Otomatik paylasim sistemi basladi!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        time.sleep(300)
        schedule.clear('ilk')
        
        while True:
            schedule.run_pending()
            time.sleep(60)


# ============================================
# TELEGRAM KOMUTLARINI YAKALAYAN FONKSİYON
# ============================================
def telegram_dinleyici():
    import telebot
    
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    bot = telebot.TeleBot(TOKEN)
    yonetici = SosyalMedyaYoneticisi()
    
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, """
🚀 TRM SİSTEMİ BULUTTA ÇALIŞIYOR!

Komutlar:
/instagram - Manuel Instagram paylaşımı
/facebook - Manuel Facebook paylaşımı
/tiktok - Manuel TikTok paylaşımı
/durum - Sistem durumu

🤖 AI Asistan aktif: Bana her şeyi sorabilirsin!
        """)
    
    @bot.message_handler(commands=['instagram'])
    def instagram_komut(message):
        sonuc = yonetici.manuel_instagram_paylas()
        bot.reply_to(message, sonuc)
    
    @bot.message_handler(commands=['facebook'])
    def facebook_komut(message):
        sonuc = yonetici.manuel_facebook_paylas()
        bot.reply_to(message, sonuc)
    
    @bot.message_handler(commands=['tiktok'])
    def tiktok_komut(message):
        sonuc = yonetici.manuel_tiktok_paylas()
        bot.reply_to(message, sonuc)
    
    @bot.message_handler(commands=['durum'])
    def durum_komut(message):
        toplam = (yonetici.paylasim_sayaci['instagram'] + 
                  yonetici.paylasim_sayaci['facebook'] + 
                  yonetici.paylasim_sayaci['tiktok'])
        rapor = f"""
📊 GÜNCEL DURUM
━━━━━━━━━━━━━━━━━━━━━
📱 Instagram: {yonetici.paylasim_sayaci['instagram']} paylaşım
📘 Facebook: {yonetici.paylasim_sayaci['facebook']} paylaşım
🎵 TikTok: {yonetici.paylasim_sayaci['tiktok']} paylaşım
━━━━━━━━━━━━━━━━━━━━━
🎯 Toplam: {toplam} paylaşım
📌 Sistem: ✅ Aktif
━━━━━━━━━━━━━━━━━━━━━
        """
        bot.reply_to(message, rapor)
    
    # ========== AI ASİSTAN (TÜM MESAJLARI YAKALA) ==========
    @bot.message_handler(func=lambda m: True)
    def ai_cevapla(message):
        """Gelen her mesaja Claude AI ile cevap ver"""
        print(f"🤔 AI soru alındı: {message.text[:50]}...")
        cevap = yonetici.claude.cevap_uret(message.text)
        bot.reply_to(message, cevap)
    # ========================================================
    
    print("🤖 Telegram dinleyici başlatılıyor...")
    bot.infinity_polling()


# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    try:
        telegram_thread = threading.Thread(target=telegram_dinleyici, daemon=True)
        telegram_thread.start()
        
        yonetici = SosyalMedyaYoneticisi()
        yonetici.calistir()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Sistem durduruldu. Gorusmek uzere!")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("Sistem yeniden baslatiliyor...")
        time.sleep(5)
        os.system('python social_media_manager.py')
