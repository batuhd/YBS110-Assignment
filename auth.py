# Çaba Shoes – Kimlik Doğrulama Modülü (auth.py)
# SHA-256 ile şifre hashleme ve doğrulama

import hashlib
import sqlite3
from database import baglanti_olustur, tablolari_olustur


def sifre_hashle(sifre):
    """Şifreyi SHA-256 ile hashler."""
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()


def giris_dogrula(kullanici_adi, sifre):
    """Kullanıcı adı ve şifreyi veritabanından doğrular."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        sifre_hash = sifre_hashle(sifre)
        imlec.execute(
            "SELECT id FROM kullanicilar WHERE kullanici_adi=? AND sifre_hash=?",
            (kullanici_adi, sifre_hash)
        )
        sonuc = imlec.fetchone()
        bag.close()
        return sonuc is not None
    except Exception as e:
        print(f"Giriş doğrulama hatası: {e}")
        return False


def varsayilan_admin_olustur():
    """Varsayılan admin hesabını oluşturur (yoksa)."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Admin var mı kontrol et
        imlec.execute("SELECT id FROM kullanicilar WHERE kullanici_adi='admin'")
        if imlec.fetchone() is None:
            # Varsayılan admin oluştur (şifre: sifre123)
            sifre_hash = sifre_hashle("sifre123")
            imlec.execute(
                "INSERT INTO kullanicilar (kullanici_adi, sifre_hash) VALUES (?, ?)",
                ("admin", sifre_hash)
            )
            bag.commit()
            print("Varsayılan admin oluşturuldu: admin / sifre123")

        bag.close()
    except Exception as e:
        print(f"Admin oluşturma hatası: {e}")


def demo_stok_yukle():
    """Demo stok verilerini yükler (stok tablosu boşsa)."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Stok tablosu boş mu kontrol et
        imlec.execute("SELECT COUNT(*) FROM stok")
        if imlec.fetchone()[0] > 0:
            bag.close()
            return

        # Demo ürünler (iç içe sözlük yapısı – nested dict)
        demo_urunler = {
            "Stiletto": {
                "renkler": {"Siyah": 1200, "Kırmızı": 1350, "Bej": 1100},
                "numaralar": [36, 37, 38, 39],
                "adet": 8
            },
            "Babet": {
                "renkler": {"Pembe": 650, "Beyaz": 600, "Siyah": 700},
                "numaralar": [36, 37, 38, 39, 40],
                "adet": 12
            },
            "Platform": {
                "renkler": {"Siyah": 1500, "Bordo": 1600},
                "numaralar": [36, 37, 38],
                "adet": 6
            },
            "Sandalet": {
                "renkler": {"Altın": 900, "Gümüş": 950, "Beyaz": 800},
                "numaralar": [36, 37, 38, 39],
                "adet": 10
            },
            "Sneaker": {
                "renkler": {"Beyaz": 1100, "Pembe": 1150, "Siyah": 1050},
                "numaralar": [37, 38, 39, 40],
                "adet": 15
            },
        }

        # Döngü ile stoka ekle (iç içe döngü – nested loop)
        for model, bilgi in demo_urunler.items():
            for renk, fiyat in bilgi["renkler"].items():
                for numara in bilgi["numaralar"]:
                    imlec.execute(
                        "INSERT INTO stok (model, renk, numara, adet, fiyat) VALUES (?, ?, ?, ?, ?)",
                        (model, renk, numara, bilgi["adet"], fiyat)
                    )

        bag.commit()
        bag.close()
        print("Demo stok verileri yüklendi.")
    except Exception as e:
        print(f"Demo stok yükleme hatası: {e}")


def demo_satis_yukle():
    """Demo satış verilerini yükler (satış tablosu boşsa)."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Satış tablosu boş mu kontrol et
        imlec.execute("SELECT COUNT(*) FROM satislar")
        if imlec.fetchone()[0] > 0:
            bag.close()
            return

        # Demo satışlar (liste yapısı)
        demo_satislar = [
            ("Stiletto", "Siyah", 37, 2, 1200, 0),
            ("Stiletto", "Kırmızı", 38, 1, 1350, 10),
            ("Babet", "Pembe", 36, 3, 650, 0),
            ("Babet", "Beyaz", 39, 1, 600, 5),
            ("Platform", "Siyah", 37, 1, 1500, 0),
            ("Sandalet", "Altın", 38, 2, 900, 15),
            ("Sneaker", "Beyaz", 39, 2, 1100, 0),
            ("Sneaker", "Pembe", 38, 1, 1150, 10),
        ]

        for model, renk, numara, adet, fiyat, indirim in demo_satislar:
            toplam = fiyat * adet * (1 - indirim / 100)
            imlec.execute(
                """INSERT INTO satislar (model, renk, numara, adet, birim_fiyat, indirim_yuzdesi, toplam_fiyat)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (model, renk, numara, adet, fiyat, indirim, toplam)
            )

        bag.commit()
        bag.close()
        print("Demo satış verileri yüklendi.")
    except Exception as e:
        print(f"Demo satış yükleme hatası: {e}")


def demo_gider_yukle():
    """Demo gider verilerini yükler (gider tablosu boşsa)."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Gider tablosu boş mu kontrol et
        imlec.execute("SELECT COUNT(*) FROM giderler")
        if imlec.fetchone()[0] > 0:
            bag.close()
            return

        # Demo giderler (liste yapısı)
        demo_giderler = [
            ("Kira", "Mağaza aylık kira bedeli", 15000),
            ("Elektrik", "Mart ayı elektrik faturası", 2500),
            ("Maaş", "Satış danışmanı maaşı", 22000),
            ("Reklam", "Instagram sponsorlu reklam", 3000),
            ("Malzeme", "Ayakkabı kutusu ve ambalaj", 1500),
            ("İnternet", "Aylık internet faturası", 800),
        ]

        for kategori, aciklama, tutar in demo_giderler:
            imlec.execute(
                "INSERT INTO giderler (kategori, aciklama, tutar) VALUES (?, ?, ?)",
                (kategori, aciklama, tutar)
            )

        bag.commit()
        bag.close()
        print("Demo gider verileri yüklendi.")
    except Exception as e:
        print(f"Demo gider yükleme hatası: {e}")


# Test amaçlı doğrudan çalıştırma
if __name__ == "__main__":
    tablolari_olustur()
    varsayilan_admin_olustur()
    print("Auth modülü hazır. Admin: admin / sifre123")
