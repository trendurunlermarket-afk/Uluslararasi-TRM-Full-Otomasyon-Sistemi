# ============================================
# TİKTOK BOTU - MANUEL PAYLAŞIM İÇİN HAZIRLIK
# ============================================

import os
import random
from datetime import datetime
import requests

class TikTokBot:
    def __init__(self):
        self.hesap_adi = os.getenv('TIKTOK_USERNAME', '@trendurunlermarket')
        self.session = requests.Session()
    
    def video_hazirla(self, urun):
        """TikTok'ta paylaşılacak video için içerik hazırlar"""
        saat = datetime.now().strftime('%H:%M')
        baslik = f"{urun['ad']} - {urun['fiyat']} TL"
        
        # Video açıklaması (hashtaglerle)
        aciklama = f"""
🔥 {baslik} 🔥

🛍️ Ürünü görmek için linke tıkla:
🔗 {urun['link']}

👇 Beğenip yorum yapmayı unutma!

#trendurunler #firsat #indirim #tiktok #{urun['kategori']}
"""
        # Video dosyası (simülasyon - gerçekte bir video dosyası olmalı)
        video_dosyasi = f"video_{urun['id']}_{saat}.mp4"
        
        print(f"🎵 TikTok: Video hazırlandı: {baslik}")
        return {
            'baslik': baslik,
            'aciklama': aciklama,
            'video': video_dosyasi,
            'zaman': saat
        }
    
    def telegram_bildirim_gonder(self, urun, video_bilgisi, telegram_bot):
        """Hazırlanan videoyu Telegram'dan size bildirir"""
        mesaj = f"""
📱 <b>TİKTOK PAYLAŞIM HAZIR!</b>
⏰ {video_bilgisi['zaman']}
👤 Hesap: {self.hesap_adi}

📦 Ürün: {urun['ad']} - {urun['fiyat']} TL
🔗 Link: {urun['link']}

📝 Açıklama:
{video_bilgisi['aciklama']}

📌 Yapılacak:
1. Bu mesajı görünce TikTok'a gir
2. Video dosyasını yükle ({video_bilgisi['video']})
3. Açıklamayı kopyala
4. Paylaş!
"""
        telegram_bot.mesaj_gonder(telegram_bot.admin_id, mesaj)
        print("📱 TikTok bildirimi Telegram'a gönderildi")
