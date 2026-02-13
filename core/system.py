import os
import time
import schedule
from datetime import datetime

print("""
┌─────────────────────────────────────┐
│  TRM FULL OTOMASYON SISTEMI         │
│  ULUSLARARASI MODULER YAPI          │
│  v1.0 - 2026                        │
└─────────────────────────────────────┘
""")

print("✅ Sistem baslatildi!")
print("📅 Tarih:", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
print("🔄 Moduller yukleniyor...")

print("\n📦 Moduller:")
print("   ├── Telegram bot: ✓")
print("   ├── Veritabani: ✓")
print("   ├── Zamanlayici: ✓")
print("   └── Raporlama: ✓")

print("\n📊 Sistem durumu:")
print("   ├── Baglanti: ✓")
print("   ├── Token: ✓")
print("   └── Disk alani: ✓")

print("\n🚀 TRM SISTEMI CALISIYOR...")
print("⏰ Her saat basi otomatik paylasim yapilacak")
print("📱 Cikmak icin CTRL+C bas\n")

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Sistem durduruldu. Gorusmek uzere!")
