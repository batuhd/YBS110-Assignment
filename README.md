# YBS110 R VE PYHTON PROGRAMLAMA DERSİ ÖDEVİ
# 👠 Çaba Shoes – Butik Yönetim Sistemi

Kadın ayakkabı butiği için geliştirilmiş masaüstü yönetim uygulaması. Stok takibi, satış kaydı, gider yönetimi ve analiz grafiklerini tek bir panelden yönetmenizi sağlar.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2-EC4899?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square)

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🔐 **Güvenli Giriş** | SHA-256 ile hashlenmiş şifre doğrulama |
| 📊 **Dashboard** | Anlık stok, model sayısı, günlük satış ve ciro kartları |
| 📦 **Stok Yönetimi** | Model, renk, numara (36-40) bazında ekleme/silme |
| 💰 **Satış Kayıt** | Cascading ComboBox ile ürün seçimi, indirim hesaplama |
| 📋 **Satış Listesi** | Pandas DataFrame ile detaylı satış raporlama |
| 💸 **Gider Takibi** | Kategorili gider ekleme, toplam/günlük özet |
| 📈 **Analiz** | Matplotlib bar chart ile model bazlı satış grafikleri + kâr-zarar özeti |

---

## 📁 Proje Yapısı

```
cabashoes/
│
├── main.py                  # Ana uygulama – AnaUygulama sınıfı + başlatıcı
├── config.py                # Tema renkleri (RENKLER sözlüğü) + ctk ayarları
├── giris_ekrani.py          # Giriş (Login) ekranı sınıfı
├── database.py              # SQLite3 veritabanı işlemleri (CRUD)
├── auth.py                  # SHA-256 kimlik doğrulama + demo veri yükleme
│
├── sayfalar/                # Sayfa modülleri (Mixin pattern)
│   ├── __init__.py
│   ├── dashboard.py         # 📊 Dashboard sayfası
│   ├── stok.py              # 📦 Stok yönetimi sayfası
│   ├── satis.py             # 💰 Satış yapma sayfası
│   ├── satislar.py          # 📋 Satış listesi sayfası
│   ├── giderler.py          # 💸 Gider takibi sayfası
│   └── analiz.py            # 📈 Analiz & grafik sayfası
│
└── cabashoes.db             # SQLite veritabanı (otomatik oluşturulur)
```

### 🏗️ Mimari

Uygulama **Mixin Pattern** kullanılarak modüler bir yapıda tasarlanmıştır. Her sayfa bağımsız bir dosyada tanımlanmış olup, `AnaUygulama` sınıfı çoklu kalıtım (multiple inheritance) ile tüm sayfa metotlarını içerir:

```mermaid
classDiagram
    class AnaUygulama {
        +sayfa_degistir(sayfa_id)
        +cikis_yap()
    }

    class DashboardMixin {
        +dashboard_goster()
    }

    class StokMixin {
        +stok_goster()
        +stok_ekle_islem()
        +stok_sil_islem()
        +stok_tablosu_guncelle()
    }

    class SatisMixin {
        +satis_goster()
        +satis_model_degisti()
        +satis_renk_degisti()
        +satis_kaydet_islem()
    }

    class SatislarMixin {
        +satislar_goster()
    }

    class GiderlerMixin {
        +giderler_goster()
        +gider_ekle_islem()
        +gider_sil_islem()
        +gider_tablosu_guncelle()
    }

    class AnalizMixin {
        +analiz_goster()
        +grafik_ayri_pencere()
    }

    AnaUygulama --|> DashboardMixin
    AnaUygulama --|> StokMixin
    AnaUygulama --|> SatisMixin
    AnaUygulama --|> SatislarMixin
    AnaUygulama --|> GiderlerMixin
    AnaUygulama --|> AnalizMixin
    AnaUygulama --|> CTk
```

### 🔄 Veri Akışı

```mermaid
flowchart LR
    A[GirisEkrani] -->|SHA-256 Doğrulama| B[AnaUygulama]
    B --> C[Dashboard]
    B --> D[Stok Yönetimi]
    B --> E[Satış Yap]
    B --> F[Satış Listesi]
    B --> G[Gider Takibi]
    B --> H[Analiz]

    D -->|CRUD| I[(SQLite3\ncabashoes.db)]
    E -->|INSERT + UPDATE| I
    G -->|INSERT + DELETE| I
    F -->|SELECT → DataFrame| I
    H -->|SELECT → Matplotlib| I
    C -->|SELECT| I
```

---

## 🛠️ Kullanılan Kütüphaneler

| Kütüphane | Sürüm | Kullanım Amacı |
|---|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | 5.2+ | Modern ve şık GUI arayüzü |
| [Pandas](https://pandas.pydata.org/) | 3.0+ | Satış verilerini DataFrame ile işleme ve raporlama |
| [Matplotlib](https://matplotlib.org/) | 3.10+ | Model bazlı satış grafikleri (bar chart) |
| **sqlite3** | Built-in | Veritabanı yönetimi (stok, satış, gider, kullanıcı) |
| **hashlib** | Built-in | SHA-256 şifre hashleme |
| **tkinter** | Built-in | Treeview tabloları ve mesaj kutuları |

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.12 veya üzeri

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/batuhd/cabashoes.git
cd cabashoes

# 2. Sanal ortam oluştur
python -m venv .venv

# 3. Sanal ortamı aktif et
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Bağımlılıkları yükle
pip install customtkinter pandas matplotlib

# 5. Uygulamayı çalıştır
python main.py
```

### Varsayılan Giriş Bilgileri

| Kullanıcı Adı | Şifre |
|---|---|
| `admin` | `sifre123` |

> İlk çalıştırmada veritabanı ve demo veriler otomatik oluşturulur.

---

## 📝 Lisans


