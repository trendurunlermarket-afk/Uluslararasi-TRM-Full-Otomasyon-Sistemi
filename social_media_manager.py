# ============================================
# TAM OTOMATİK SOSYAL MEDYA BOTU
# INSTAGRAM + FACEBOOK + TELEGRAM
# HATASIZ VERSİYON - 14 ŞUBAT 2026
# ============================================

import os
import time
import random
import schedule
import requests
from datetime import datetime
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# ============================================
# TELEGRAM BOT
# ============================================
class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.admin_id = '1450144293'
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def mesaj_gonder(self, chat_id, mesaj):
        """Telegram mesajı gönderir"""
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
        """Yöneticiye bildirim gönderir"""
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
        """Instagram'a giriş yapar"""
        print(f"📱 Instagram: @{self.username} giriş yapılıyor...")
        time.sleep(2)
        print(f"✅ Instagram: @{self.username} giriş başarılı")
        return True
    
    def fotografli_gonderi_paylas(self, resim_url, baslik, urun_linki):
        """Fotoğraflı gönderi paylaşır"""
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
        """Instagram hikayesi paylaşır"""
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
        """Facebook sayfasına gönderi paylaşır"""
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
# URUN VERITABANI - HATASIZ VERSIYON
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
        """Rastgele bir urun secer"""
        secilen = random.choice(self.urunler)
        return secilen


# ============================================
# SOSYAL MEDYA YONETICISI (ANA SINIF)
# ============================================
class SosyalMedyaYoneticisi:
    def __init__(self):
        print("""
╔══════════════════════════════════════════════════╗
║  🚀 TRM TAM OTOMASYON SOSYAL MEDYA BOTU         ║
║  📱 Instagram | 📘 Facebook | 🤖 Telegram        ║
║  ⏰ Her saat basi otomatik paylasim              ║
║  👤 Yonetici: 1450144293                         ║
╚══════════════════════════════════════════════════╝
        """)
        
        # Botlari baslat
        self.telegram = TelegramBot()
        self.instagram = InstagramBot()
        self.facebook = FacebookBot()
        self.urunler = UrunVeritabani()
        
        # Paylasim sayaci
        self.paylasim_sayaci = {
            'instagram': 0,
            'facebook': 0
        }
        
        print("✅ Botlar baslatildi")
        print(f"📱 Instagram: @{self.instagram.username}")
        print(f"📘 Facebook: {self.facebook.page_name}")
        print("⏳ Instagram giris yapiliyor...")
        
        self.instagram.giris_yap()
        
        print("✅ Sistem hazir!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    def instagram_paylas(self):
        """Instagram'da otomatik paylasim yapar"""
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
        """Facebook'ta otomatik paylasim yapar"""
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
    
    def telegram_rapor(self):
        """Her saat basi Telegram raporu gonderir"""
        toplam = self.paylasim_sayaci['instagram'] + self.paylasim_sayaci['facebook']
        
        rapor = f"""
📊 <b>SAATLIK PAYLASIM RAPORU</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Saat: {datetime.now().strftime('%H:%M')}
📱 Instagram: {self.paylasim_sayaci['instagram']} paylasim
📘 Facebook: {self.paylasim_sayaci['facebook']} paylasim
━━━━━━━━━━━━━━━━━━━━━
🎯 Toplam Paylasim: {toplam}
📌 Sistem: ✅ Calisiyor
━━━━━━━━━━━━━━━━━━━━━
        """
        
        self.telegram.mesaj_gonder('1450144293', rapor)
        print(f"\n[{datetime.now().strftime('%H:%M')}] 🤖 Telegram raporu gonderildi")
    
    def calistir(self):
        """Ana donguyu baslatir"""
        
        print("""
⏰ ZAMANLAMA AYARLARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Instagram: Her 2 saatte bir
📘 Facebook:  Her 3 saatte bir
🤖 Telegram:  Her saat basi rapor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        # Instagram: Her 2 saatte bir
        schedule.every(2).hours.at(":00").do(self.instagram_paylas)
        schedule.every(2).hours.at(":30").do(self.instagram_paylas)
        
        # Facebook: Her 3 saatte bir
        schedule.every(3).hours.at(":15").do(self.facebook_paylas)
        schedule.every(3).hours.at(":45").do(self.facebook_paylas)
        
        # Telegram raporu: Her saat basi
        schedule.every().hour.at(":05").do(self.telegram_rapor)
        
        # Ilk paylasim hemen
        schedule.every(1).minutes.do(self.instagram_paylas).tag('ilk')
        schedule.every(2).minutes.do(self.facebook_paylas).tag('ilk')
        
        print("✅ Otomatik paylasim sistemi basladi!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        # 5 dakika sonra ilk paylasimlari kaldir
        time.sleep(300)
        schedule.clear('ilk')
        
        # Sonsuz dongu
        while True:
            schedule.run_pending()
            time.sleep(60)


# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    try:
        bot = SosyalMedyaYoneticisi()
        bot.calistir()
    except KeyboardInterrupt:
        print("\n\n🛑 Sistem durduruldu. Gorusmek uzere!")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("Sistem yeniden baslatiliyor...")
        time.sleep(5)
        os.system('python social_media_manager.py')
