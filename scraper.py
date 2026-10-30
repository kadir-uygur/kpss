import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SPOR_KEYWORDS = [
    "beden eğitimi", "besyo", "spor bilimleri", "spor uzmanı", 
    "antrenör", "rekreasyon", "egzersiz", "cankurtaran", "can kurtaran", "gençlik ve spor"
]

GENEL_KEYWORDS = [
    "4001", "herhangi bir lisans", "tüm lisans", "zabıta", "itfaiye", "büro personeli", "yurt yönetim"
]

def get_category(title, source):
    t = title.lower()
    if any(k in t for k in SPOR_KEYWORDS):
        return "spor"
    if "malatya" in source.lower() or "malatya" in t:
        return "malatya"
    if any(k in t for k in GENEL_KEYWORDS):
        return "genel"
    return None

def scrape_memurlar():
    ads = []
    try:
        url = "https://ilan.memurlar.net/default.aspx"
        res = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            title = a.get_text(strip=True)
            if "/ilan/" in href and len(title) > 10:
                full_url = f"https://ilan.memurlar.net{href}" if href.startswith("/") else href
                cat = get_category(title, "Memurlar.net")
                if cat:
                    ads.append({
                        "title": title,
                        "link": full_url,
                        "source": "Memurlar.net",
                        "category": cat,
                        "date": datetime.now().strftime("%d.%m.%Y")
                    })
    except Exception as e:
        print(f"Memurlar hatası: {e}")
    return ads

def scrape_malatya_meb():
    ads = []
    try:
        url = "https://malatya.meb.gov.tr/www/duyurular/kategori/2"
        res = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            title = a.get_text(strip=True)
            if "icerik" in href and len(title) > 8:
                full_url = f"https://malatya.meb.gov.tr{href}" if href.startswith("/") else href
                ads.append({
                    "title": title,
                    "link": full_url,
                    "source": "Malatya MEM",
                    "category": "malatya",
                    "date": datetime.now().strftime("%d.%m.%Y")
                })
    except Exception as e:
        print(f"Malatya MEB hatası: {e}")
    return ads

def scrape_malatya_bel():
    ads = []
    try:
        url = "https://www.malatya.bel.tr/duyurular"
        res = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            title = a.get_text(strip=True)
            if ("/duyuru/" in href or "ilan" in href) and len(title) > 8:
                full_url = f"https://www.malatya.bel.tr{href}" if href.startswith("/") else href
                ads.append({
                    "title": title,
                    "link": full_url,
                    "source": "Malatya Belediyesi",
                    "category": "malatya",
                    "date": datetime.now().strftime("%d.%m.%Y")
                })
    except Exception as e:
        print(f"Malatya Bel hatası: {e}")
    return ads

def scrape_kamuilan():
    ads = []
    try:
        url = "https://kamuilan.sbb.gov.tr/"
        res = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"]
            if len(title) > 15:
                cat = get_category(title, "SBB Kamu İlan")
                if cat:
                    ads.append({
                        "title": title,
                        "link": href if href.startswith("http") else url,
                        "source": "SBB Kamu İlan",
                        "category": cat,
                        "date": datetime.now().strftime("%d.%m.%Y")
                    })
    except Exception as e:
        print(f"SBB hatası: {e}")
    return ads

def main():
    raw_ads = scrape_memurlar() + scrape_malatya_meb() + scrape_malatya_bel() + scrape_kamuilan()
    
    # Tekrarlayan bağlantıları temizle
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
    print(f"Toplam {len(unique_ads)} ilan kaydedildi.")

if __name__ == "__main__":
    main()
