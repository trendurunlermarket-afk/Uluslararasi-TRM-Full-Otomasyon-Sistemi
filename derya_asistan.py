# ============================================
# DERYA ASİSTAN - Engelli Ekip + Form Doldurma
# ============================================

import os
import csv
import sqlite3
from datetime import datetime

class DeryaAsistan:
    def __init__(self):
        self.ekip_dosyasi = "ekip_listesi.csv"
        self.veritabani = "satislar.db"
        self._veritabani_hazirla()
    
    def _veritabani_hazirla(self):
        conn = sqlite3.connect(self.veritabani)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ekip_uyeleri
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      ad TEXT,
                      engel_durumu TEXT,
                      platform TEXT,
                      hesap_adi TEXT,
                      iban TEXT,
                      komisyon_orani REAL,
                      kayit_tarihi TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS satislar
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      uye_id INTEGER,
                      urun_adi TEXT,
                      tutar REAL,
                      komisyon REAL,
                      tarih TEXT)''')
        conn.commit()
        conn.close()
    
    def ekip_ekle(self, ad, engel, platform, hesap, iban, komisyon):
        conn = sqlite3.connect(self.veritabani)
        c = conn.cursor()
        c.execute('''INSERT INTO ekip_uyeleri 
                     (ad, engel_durumu, platform, hesap_adi, iban, komisyon_orani, kayit_tarihi)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (ad, engel, platform, hesap, iban, komisyon, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        print(f"✅ {ad} ekip listesine eklendi.")
    
    def satis_ekle(self, uye_id, urun_adi, tutar):
        # Önce üyenin komisyon oranını bul
        conn = sqlite3.connect(self.veritabani)
        c = conn.cursor()
        c.execute("SELECT komisyon_orani FROM ekip_uyeleri WHERE id=?", (uye_id,))
        sonuc = c.fetchone()
        if not sonuc:
            print(f"❌ Üye ID {uye_id} bulunamadı.")
            return
        komisyon_orani = sonuc[0]
        komisyon = tutar * komisyon_orani / 100
        
        c.execute('''INSERT INTO satislar (uye_id, urun_adi, tutar, komisyon, tarih)
                     VALUES (?, ?, ?, ?, ?)''',
                  (uye_id, urun_adi, tutar, komisyon, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
        conn.close()
        print(f"💰 Satış eklendi! Üye {uye_id} için {komisyon:.2f} TL komisyon.")
    
    def aylik_rapor(self, ay, yil):
        conn = sqlite3.connect(self.veritabani)
        c = conn.cursor()
        c.execute('''SELECT uye_id, SUM(komisyon) FROM satislar 
                     WHERE strftime('%m', tarih)=? AND strftime('%Y', tarih)=?
                     GROUP BY uye_id''', (ay, yil))
        satirlar = c.fetchall()
        print(f"\n📊 {ay}/{yil} AYLIK KOMİSYON RAPORU")
        print("="*40)
        toplam = 0
        for uye_id, komisyon in satirlar:
            c.execute("SELECT ad, iban FROM ekip_uyeleri WHERE id=?", (uye_id,))
            ad, iban = c.fetchone()
            print(f"👤 {ad}: {komisyon:.2f} TL (IBAN: {iban})")
            toplam += komisyon
        print("="*40)
        print(f"TOPLAM: {toplam:.2f} TL")
        conn.close()
    
    def form_doldur(self, form_adi, alanlar):
        """Talimatla form doldurma simülasyonu"""
        print(f"📝 {form_adi} formu dolduruluyor...")
        for alan, deger in alanlar.items():
            print(f"   {alan}: {deger}")
        print("✅ Form dolduruldu.")

if __name__ == "__main__":
    asistan = DeryaAsistan()
    asistan.ekip_ekle("Ali Yılmaz", "Görme engelli", "Instagram", "@ali_fashion", "TR123456", 20)
    asistan.satis_ekle(1, "Akıllı Bileklik", 449)
    asistan.aylik_rapor("02", "2026")
    asistan.form_doldur("Instagram Reklam Formu", {
        "Hedef Kitle": "25-45 yaş kadınlar",
        "Bütçe": "50 TL",
        "Süre": "7 gün"
    })
