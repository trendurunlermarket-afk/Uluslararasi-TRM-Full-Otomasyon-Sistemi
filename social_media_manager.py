# social_media_manager.py
from telegram_bot import TelegramBot
from instagram_bot import InstagramBot
from facebook_bot import FacebookBot
import schedule
import time
import random

class SocialMediaManager:
    def __init__(self):
        self.telegram = TelegramBot()
        self.instagram = InstagramBot("kullanici_adi", "sifre")
        self.facebook = FacebookBot("access_token", "sayfa_id")
        self.platformlar = []
    
    def platform_ekle(self, platform_adi, bot_nesnesi):
        """Yeni bir sosyal medya platformu ekler"""
        self.platformlar.append({
            'ad': platform_adi,
            'bot': bot_nesnesi
        })
        print(f"✅ {platform_adi} sisteme eklendi")
    
    def herkese_paylas(self, urun_bilgisi):
        """Tüm platformlarda aynı anda paylaşım yapar"""
        
        basarili = 0
        basarisiz = 0
        
        for platform in self.platformlar:
            try:
                if platform['ad'] == 'Instagram':
                    platform['bot'].fotografli_gonderi_paylas(
                        urun_bilgisi['foto_yolu'],
                        urun_bilgisi['aciklama']
                    )
                elif platform['ad'] == 'Facebook':
                    platform['bot'].sayfa_gonderisi_paylas(
                        urun_bilgisi['aciklama'],
                        urun_bilgisi['link']
                    )
                elif platform['ad'] == 'Telegram':
                    platform['bot'].kanala_mesaj_gonder(
                        urun_bilgisi['aciklama']
                    )
                basarili += 1
            except:
                basarisiz += 1
        
        print(f"📊 Paylaşım raporu: {basarili} başarılı, {basarisiz} başarısız")
        return basarili, basarisiz
    
    def otomatik_paylasim_baslat(self, urun_listesi, saat_araligi=2):
        """Belirli aralıklarla otomatik paylaşım başlatır"""
        
        def paylasim_yap():
            urun = random.choice(urun_listesi)
            self.herkese_paylas(urun)
        
        schedule.every(saat_araligi).hours.do(paylasim_yap)
        print(f"✅ Otomatik paylaşım başladı (Her {saat_araligi} saatte bir)")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
