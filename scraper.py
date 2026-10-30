import json
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Sunucuların botu kilitlemesini önleyen güvenli süre sınırı (bağlantı 3 sn, okuma 5 sn)
TIMEOUT = (3.0, 5.0)

# 1. Filtre Kelimeleri
SPOR_KEYWORDS = [
    "beden eğitimi", "besyo", "spor bilimleri", "spor uzmanı", 
    "antrenör", "rekreasyon", "egzersiz", "cankurtaran", "can kurtaran", 
    "gençlik ve spor", "yurt yönetim", "öğretmen subay", "gençlik lideri", "yurt yönetim", "spor masörü", "tenis antrenör", "kickboks antrenör"
]

GENEL_KEYWORDS = [
    "4001", "herhangi bir lisans", "tüm lisans", "zabıta", "itfaiye", 
    "büro personeli", "subay", "astsubay", "jandarma", "sahil güvenlik", 
    "araştırma görevlisi", "öğretim görevlisi", "infaz ve koruma", "gardiyan", "pomem", "polis", "gümrük muhafaza", "bekçi"
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_category(title, source):
    t = title.lower()
    s = source.lower()
    if any(k in t for k in SPOR_KEYWORDS):
        return "spor"
    if any(k in t for k in ["malatya", "inönü", "turgut özal", "fırat", "battalgazi", "yeşilyurt"]) or "malatya" in s:
        return "malatya"
    if any(k in t for k in GENEL_KEYWORDS):
        return "genel"
    return None

def fetch_ads(url, link_filter, source_name, is_relative=True, base_url=""):
    ads = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                title = a.get_text(strip=True)
                if link_filter in href and len(title) > 8:
                    full_url = f"{base_url}{href}" if is_relative and href.startswith("/") else href
                    cat = get_category(title, source_name)
                    if cat:
                        ads.append({
                            "title": title,
                            "link": full_url,
                            "source": source_name,
                            "category": cat,
                            "date": datetime.now().strftime("%d.%m.%Y")
                        })
            log(f"-> {source_name} tamamlandı ({len(ads)} uygun ilan)")
    except Exception:
        log(f"-> {source_name} atlandı (Bağlantı zaman aşımı veya erişim kısıtı)")
    return ads

def main():
    log("Tüm kamu, üniversite ve bakanlık taraması başlatılıyor...")
    raw_ads = []

    # 1. Merkezi Memurlar.net (Genel Kamu İlanları)
    raw_ads += fetch_ads(
        "https://ilan.memurlar.net/default.aspx", 
        "/ilan/", "Memurlar Kamu", base_url="https://ilan.memurlar.net"
    )

    # 2. Askeri, Güvenlik ve Emniyet İlanları (MSB, Jandarma Subaylık/Astsubaylık vb.)
    raw_ads += fetch_ads(
        "https://ilan.memurlar.net/kategori/askeri-ve-guvenlik-ilanlari/", 
        "/ilan/", "Askeri / Emniyet", base_url="https://ilan.memurlar.net"
    )

    # 3. Üniversite Akademik Kadro İlanları (Araştırma & Öğretim Görevlisi)
    raw_ads += fetch_ads(
        "https://ilan.memurlar.net/kategori/akademik-kadro-ilanlari/", 
        "/ilan/", "Akademik Kadro", base_url="https://ilan.memurlar.net"
    )

    # 4. Gençlik ve Spor Bakanlığı (GSB Ana Sayfa + Personel GM)
    raw_ads += fetch_ads(
        "https://www.gsb.gov.tr/duyurular.html", 
        "duyuru", "GSB Duyurular", base_url="https://www.gsb.gov.tr"
    )
    raw_ads += fetch_ads(
        "https://pgm.gsb.gov.tr/Duyurular", 
        "Duyuru", "GSB Personel GM", base_url="https://pgm.gsb.gov.tr"
    )

    # 5. Yerel Üniversiteler (İnönü, Turgut Özal, Fırat)
    raw_ads += fetch_ads(
        "https://www.inonu.edu.tr/tr/duyurular", 
        "duyuru", "İnönü Üni", base_url="https://www.inonu.edu.tr"
    )
    raw_ads += fetch_ads(
        "https://ozal.edu.tr/tr/duyurular", 
        "duyuru", "Turgut Özal Üni", base_url="https://ozal.edu.tr"
    )
    raw_ads += fetch_ads(
        "https://www.firat.edu.tr/tr/duyurular", 
        "duyuru", "Fırat Üni", base_url="https://www.firat.edu.tr"
    )

    # 6. Malatya Yerel Duyuruları (MEM & Büyükşehir Belediyesi)
    raw_ads += fetch_ads(
        "https://malatya.meb.gov.tr/www/duyurular/kategori/2", 
        "icerik", "Malatya MEM", base_url="https://malatya.meb.gov.tr"
    )
    raw_ads += fetch_ads(
        "https://www.malatya.bel.tr/duyurular", 
        "duyuru", "Malatya Bel", base_url="https://www.malatya.bel.tr"
    )
    

    # Tekrarlayan bağlantıları temizle (Duplicate engelleme)
    unique_ads = {}
    for ad in raw_ads:
        if ad["link"] not in unique_ads:
            unique_ads[ad["link"]] = ad

    output = {
        "last_updated": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "total_count": len(unique_ads),
        "ilanlar": list(unique_ads.values())
    }

    with open("ilanlar.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log(f"İşlem başarıyla tamamlandı! Toplam {len(unique_ads)} ilan kaydedildi.")

if __name__ == "__main__":
    main()
