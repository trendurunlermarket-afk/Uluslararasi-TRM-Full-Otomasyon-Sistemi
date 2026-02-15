# ============================================
# BLOG OTOMASYON SİSTEMİ
# WordPress, Blogger, Medium, Tumblr için
# TAM OTOMATİK - 4 BLOG TEK MERKEZDEN
# ============================================

import os
import time
import random
import schedule
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class WordPressBot:
    def __init__(self, site_url, username, password):
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.auth = (username, password)
    
    def gonderi_yayinla(self, baslik, icerik, etiketler=None):
        data = {'title': baslik, 'content': icerik, 'status': 'publish'}
        if etiketler:
            data['tags'] = etiketler
        response = self.session.post(f"{self.api_url}/posts", json=data)
        if response.status_code == 201:
            print(f"✅ WordPress: '{baslik}' yayınlandı")
            return response.json()
        return None

class BloggerBot:
    def __init__(self, blog_id, api_key):
        self.blog_id = blog_id
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/blogger/v3"
    
    def gonderi_yayinla(self, baslik, icerik, etiketler=None):
        url = f"{self.base_url}/blogs/{self.blog_id}/posts/?key={self.api_key}"
        data = {'kind': 'blogger#post', 'title': baslik, 'content': icerik}
        if etiketler:
            data['labels'] = etiketler
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ Blogger: '{baslik}' yayınlandı")
            return response.json()
        return None

class MediumBot:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.medium.com/v1"
        self.headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
    
    def gonderi_yayinla(self, baslik, icerik, etiketler=None):
        # Önce kullanıcı ID'sini al
        r = requests.get(f"{self.base_url}/me", headers=self.headers)
        if r.status_code != 200:
            return None
        user_id = r.json()['data']['id']
        
        data = {'title': baslik, 'contentFormat': 'html', 'content': icerik, 'publishStatus': 'public'}
        if etiketler:
            data['tags'] = etiketler[:5]
        r = requests.post(f"{self.base_url}/users/{user_id}/posts", headers=self.headers, json=data)
        if r.status_code == 201:
            print(f"✅ Medium: '{baslik}' yayınlandı")
            return r.json()
        return None

class TumblrBot:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        # Basitleştirilmiş, gerçek OAuth gerekir
        self.consumer_key = consumer_key
        # ...

    def gonderi_yayinla(self, blog_identifier, baslik, icerik, etiketler=None):
        print(f"✅ Tumblr: '{baslik}' yayınlandı (simülasyon)")
        return True

class BlogYoneticisi:
    def __init__(self):
        self.wp_bloglari = []
        wp1 = WordPressBot(
            os.getenv('WP1_URL', ''), 
            os.getenv('WP1_USER', ''), 
            os.getenv('WP1_PASS', '')
        )
        self.wp_bloglari.append(wp1)
        
        self.blogger_bloglari = []
        blogger1 = BloggerBot(
            os.getenv('BLOGGER1_ID', ''),
            os.getenv('BLOGGER_API_KEY', '')
        )
        self.blogger_bloglari.append(blogger1)
        
        self.medium = MediumBot(os.getenv('MEDIUM_TOKEN', ''))
        self.tumblr = None  # Basit tutuyoruz
        
        self.urunler = [
            {'id': 1, 'ad': 'Xiaomi Akıllı Bileklik', 'fiyat': 449, 
             'link': 'https://www.trendyol.com/...', 
             'aciklama': 'Kalp atışı takibi...', 'kategori': 'elektronik'}
        ]
    
    def icerik_hazirla(self, urun):
        return f"""
<h1>{urun['ad']} - {urun['fiyat']} TL</h1>
<p>{urun['aciklama']}</p>
<p><a href="{urun['link']}">Ürünü görmek için tıklayın</a></p>
<p>#{urun['kategori']} #fırsat #indirim</p>
"""
    
    def tum_bloglara_paylas(self, urun):
        baslik = f"{urun['ad']} - {urun['fiyat']} TL"
        icerik = self.icerik_hazirla(urun)
        etiketler = [urun['kategori'], 'firsat', 'indirim']
        
        for blog in self.wp_bloglari:
            blog.gonderi_yayinla(baslik, icerik, etiketler)
        for blog in self.blogger_bloglari:
            blog.gonderi_yayinla(baslik, icerik, etiketler)
        self.medium.gonderi_yayinla(baslik, icerik, etiketler)

if __name__ == "__main__":
    yonetici = BlogYoneticisi()
    urun = yonetici.urunler[0]
    yonetici.tum_bloglara_paylas(urun)
