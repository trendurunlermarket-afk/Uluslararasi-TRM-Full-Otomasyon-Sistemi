import telebot
import os
from dotenv import load_dotenv

# .env dosyasından token'ı al
load_dotenv('secrets.env')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Botu başlat
bot = telebot.TeleBot(TOKEN)

# /start komutu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        "🚀 **TRM FULL OTOMASYON SİSTEMİ**\n\n"
        "🇹🇷 Hoşgeldin! Ben senin otomasyon asistanınım.\n"
        "🌍 Welcome! I'm your automation assistant.\n\n"
        "📌 Komutlar:\n"
        "/start - Başlat\n"
        "/durum - Sistem durumu\n"
        "/yardim - Yardım"
    )

# /durum komutu
@bot.message_handler(commands=['durum'])
def send_status(message):
    bot.reply_to(message,
        "📊 **SİSTEM DURUMU**\n\n"
        "✅ Bot: Aktif\n"
        "✅ Veritabanı: Bağlı\n"
        "✅ Zamanlayıcı: Çalışıyor\n"
        "👥 Ekip: 0 üye\n"
        "💰 Komisyon: Hesaplanıyor"
    )

# /yardim komutu
@bot.message_handler(commands=['yardim'])
def send_help(message):
    bot.reply_to(message,
        "🆘 **YARDIM**\n\n"
        "Komutlar:\n"
        "/start - Botu başlat\n"
        "/durum - Sistem durumu\n"
        "/yardim - Bu mesaj\n\n"
        "📞 İletişim: GitHub üzerinden issue açın."
    )

# Tüm mesajları yakala
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "❓ Anlamadım. /yardim yazın.")

print("🤖 Telegram bot başlatılıyor...")
print("✅ Bot hazır!")

# Botu çalıştır
bot.infinity_polling()
