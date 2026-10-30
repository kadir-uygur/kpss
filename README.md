# 🎯 KPSS & Kamu İlan Takip Portalı

![GitHub Actions Workflow Status](https://img.shields.io/badge/Workflow-GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/Hosting-GitHub_Pages-222222?style=flat&logo=githubpages&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/UI-Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Kamu kurumlarının, bakanlıkların ve üniversitelerin dağınık yapıda yayımladığı iş/kadro ilanlarını merkezi tek bir noktadan takip etmek amacıyla geliştirilmiş, **sıfır sunucu maliyetli (serverless)** ve tam otomatik web portalı.

Sistem; Beden Eğitimi ve Spor (BESYO), 4001 Genel Lisans kadroları (Zabıta, İtfaiye, Büro vb.), askeri/güvenlik alımları ve Malatya yerel duyurularını düzenli olarak tarar, filtrelenmiş verileri modern bir arayüzde kullanıma sunar.

🔗 **Canlı Demo:** [kadir-uygur.github.io/kpss](https://kadir-uygur.github.io/kpss/)

---

## 🚀 Öne Çıkan Özellikler

* **7/24 Bağımsız Otomasyon:** Herhangi bir fiziksel sunucu veya açık bilgisayar gerektirmeden, **GitHub Actions** cron döngüleri ile periyodik olarak arka planda çalışır.
* **Akıllı Filtreleme Algoritması:** Yayımlanan duyuru başlıklarını anahtar kelime eşleştirmesi ile analiz eder; Spor/BESYO, Malatya Yerel ve Genel Lisans olarak otomatik kategorize eder.
* **Hafif ve Hızlı Arayüz:** Vanilla JS ve Tailwind CSS ile inşa edilmiştir; verileri asenkron (`ilanlar.json`) okuyarak anlık canlı arama ve filtreleme sağlar.
* **Mobil Uyumlu (PWA Desteği):** Mobil tarayıcılardan "Ana Ekrana Ekle" özelliğiyle doğrudan yerel bir mobil uygulama gibi kullanılabilir.

---

## 🛠️ Sistem Mimarisi

[Resmi Kurum & İlan Siteleri]
│
▼  (Her 3 saatte bir)
[GitHub Actions (Ubuntu)] ──> [scraper.py (Python/BeautifulSoup)]
│
▼
[ilanlar.json Dosyasının Güncellenmesi]
│
▼
[GitHub Pages Deployment] ──> [index.html (Tailwind CSS Arayüzü)]


---

## 📌 Taranan Kaynaklar

Portal, aşağıdaki kurum ve portalların duyuru ve ilan sayfalarını anlık olarak izler:

1. **Merkezi Platformlar:** Memurlar.net (Kamu, Askeri/Emniyet ve Akademik Kadro İlanları)
2. **Bakanlıklar:** Gençlik ve Spor Bakanlığı (GSB Ana Sayfa & Personel Genel Müdürlüğü)
3. **Bölgesel Üniversiteler:** İnönü Üniversitesi, Malatya Turgut Özal Üniversitesi, Fırat Üniversitesi
4. **Yerel Yönetimler:** Malatya İl Millî Eğitim Müdürlüğü, Malatya Büyükşehir Belediyesi

---

## 💻 Kullanılan Teknolojiler

* **Veri Kazıma & İşleme:** Python 3.11, `requests`, `beautifulsoup4`
* **Otomasyon & CI/CD:** GitHub Actions (Scheduled Workflows)
* **Ön Yüz:** HTML5, Modern CSS (Tailwind CDN), FontAwesome Icons, JavaScript (Fetch API)
* **Barındırma & Yayın:** GitHub Pages

---

## ⚙️ Yerel Kurulum (Local Development)

Projeyi kendi bilgisayarınızda çalıştırmak için:

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/kadir-uygur/kpss.git](https://github.com/kadir-uygur/kpss.git)
   cd kpss
Gerekli Python kütüphanelerini kurun:
pip install requests beautifulsoup4

Veri çekiciyi çalıştırarak ilanlar.json dosyasını oluşturun:
python scraper.py


index.html dosyasını herhangi bir web tarayıcısında açın.
