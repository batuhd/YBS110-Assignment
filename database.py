# Çaba Shoes – Veritabanı Modülü (database.py)
# SQLite3 veritabanı işlemleri: stok, satış, gider tabloları

import sqlite3
import os

# Veritabanı dosya yolu (proje klasöründe)
VT_DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cabashoes.db")


def baglanti_olustur():
    """Veritabanı bağlantısı oluşturur ve döndürür."""
    bag = sqlite3.connect(VT_DOSYA)
    return bag


def tablolari_olustur():
    """Gerekli tabloları oluşturur (yoksa oluşturur)."""
    bag = baglanti_olustur()
    imlec = bag.cursor()

    # Kullanıcılar tablosu
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT UNIQUE NOT NULL,
            sifre_hash TEXT NOT NULL
        )
    """)

    # Stok tablosu
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            renk TEXT NOT NULL,
            numara INTEGER NOT NULL,
            adet INTEGER NOT NULL DEFAULT 0,
            fiyat REAL NOT NULL DEFAULT 0.0
        )
    """)

    # Satışlar tablosu
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS satislar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            renk TEXT NOT NULL,
            numara INTEGER NOT NULL,
            adet INTEGER NOT NULL,
            birim_fiyat REAL NOT NULL,
            indirim_yuzdesi REAL DEFAULT 0,
            toplam_fiyat REAL NOT NULL,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Giderler tablosu
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS giderler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT NOT NULL,
            aciklama TEXT NOT NULL,
            tutar REAL NOT NULL,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    bag.commit()
    bag.close()


# STOK İŞLEMLERİ (CRUD – Ekle, Oku, Güncelle, Sil)

def stok_ekle(model, renk, numara, adet, fiyat):
    """Stoka yeni ürün ekler veya mevcut ürünün adedini artırır."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Aynı model, renk ve numarada ürün var mı kontrol et
        imlec.execute(
            "SELECT id, adet FROM stok WHERE model=? AND renk=? AND numara=?",
            (model, renk, numara)
        )
        mevcut = imlec.fetchone()

        if mevcut:
            # Varsa adedi güncelle
            yeni_adet = mevcut[1] + adet
            imlec.execute("UPDATE stok SET adet=?, fiyat=? WHERE id=?",
                         (yeni_adet, fiyat, mevcut[0]))
        else:
            # Yoksa yeni kayıt ekle
            imlec.execute(
                "INSERT INTO stok (model, renk, numara, adet, fiyat) VALUES (?, ?, ?, ?, ?)",
                (model, renk, numara, adet, fiyat)
            )

        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Stok ekleme hatası: {e}")
        return False


def tum_stoklari_getir():
    """Tüm stok kayıtlarını liste olarak döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT id, model, renk, numara, adet, fiyat FROM stok ORDER BY model, renk, numara")
        stoklar = imlec.fetchall()
        bag.close()
        return stoklar
    except Exception as e:
        print(f"Stok getirme hatası: {e}")
        return []


def stok_sil(stok_id):
    """Belirtilen ID'ye sahip stok kaydını siler."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("DELETE FROM stok WHERE id=?", (stok_id,))
        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Stok silme hatası: {e}")
        return False


def stok_guncelle(stok_id, model, renk, numara, adet, fiyat):
    """Belirtilen ID'ye sahip stok kaydını günceller."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "UPDATE stok SET model=?, renk=?, numara=?, adet=?, fiyat=? WHERE id=?",
            (model, renk, numara, adet, fiyat, stok_id)
        )
        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Stok güncelleme hatası: {e}")
        return False


def stok_bilgisi_getir(model, renk, numara):
    """Belirli bir ürünün stok bilgisini döndürür (adet, fiyat)."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "SELECT adet, numara, fiyat FROM stok WHERE model=? AND renk=? AND numara=?",
            (model, renk, numara)
        )
        bilgi = imlec.fetchone()
        bag.close()
        return bilgi
    except Exception as e:
        print(f"Stok bilgisi getirme hatası: {e}")
        return None


# SATIŞ İŞLEMLERİ

def satis_kaydet(model, renk, numara, adet, birim_fiyat, indirim_yuzdesi):
    """Satış kaydı oluşturur ve stoktan düşer."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()

        # Stok kontrolü
        imlec.execute(
            "SELECT id, adet FROM stok WHERE model=? AND renk=? AND numara=?",
            (model, renk, numara)
        )
        stok = imlec.fetchone()

        if not stok or stok[1] < adet:
            bag.close()
            return False

        # Toplam fiyat hesaplama (indirimli)
        toplam_fiyat = birim_fiyat * adet * (1 - indirim_yuzdesi / 100)

        # Satış kaydı ekle
        imlec.execute(
            """INSERT INTO satislar (model, renk, numara, adet, birim_fiyat, indirim_yuzdesi, toplam_fiyat)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (model, renk, numara, adet, birim_fiyat, indirim_yuzdesi, toplam_fiyat)
        )

        # Stoktan düş
        yeni_adet = stok[1] - adet
        if yeni_adet <= 0:
            imlec.execute("DELETE FROM stok WHERE id=?", (stok[0],))
        else:
            imlec.execute("UPDATE stok SET adet=? WHERE id=?", (yeni_adet, stok[0]))

        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Satış kaydetme hatası: {e}")
        return False


def tum_satislari_getir():
    """Tüm satış kayıtlarını liste olarak döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            """SELECT id, model, renk, numara, adet, birim_fiyat, indirim_yuzdesi, toplam_fiyat, tarih
               FROM satislar ORDER BY tarih DESC"""
        )
        satislar = imlec.fetchall()
        bag.close()
        return satislar
    except Exception as e:
        print(f"Satış getirme hatası: {e}")
        return []


# DASHBOARD VERİLERİ

def toplam_stok_sayisi():
    """Toplam stok adedini döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT COALESCE(SUM(adet), 0) FROM stok")
        sonuc = imlec.fetchone()[0]
        bag.close()
        return sonuc
    except Exception as e:
        print(f"Toplam stok hatası: {e}")
        return 0


def toplam_model_sayisi():
    """Benzersiz model sayısını döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT COUNT(DISTINCT model) FROM stok")
        sonuc = imlec.fetchone()[0]
        bag.close()
        return sonuc
    except Exception as e:
        print(f"Model sayısı hatası: {e}")
        return 0


def gunluk_satis_ozeti():
    """Bugünkü satış adedi ve ciroyu döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            """SELECT COALESCE(SUM(adet), 0), COALESCE(SUM(toplam_fiyat), 0)
               FROM satislar WHERE DATE(tarih) = DATE('now')"""
        )
        sonuc = imlec.fetchone()
        bag.close()
        return sonuc[0], sonuc[1]
    except Exception as e:
        print(f"Günlük satış hatası: {e}")
        return 0, 0.0


def model_bazli_satis():
    """Model bazlı toplam satış adetlerini sözlük olarak döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            """SELECT model, SUM(adet) as toplam_adet
               FROM satislar GROUP BY model ORDER BY toplam_adet DESC"""
        )
        sonuclar = imlec.fetchall()
        bag.close()

        # Sözlük yapısına dönüştür
        satis_sozluk = {}
        for model, adet in sonuclar:
            satis_sozluk[model] = adet
        return satis_sozluk
    except Exception as e:
        print(f"Model bazlı satış hatası: {e}")
        return {}


def benzersiz_modeller():
    """Stoktaki benzersiz model isimlerini liste olarak döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT DISTINCT model FROM stok WHERE adet > 0 ORDER BY model")
        modeller = [satir[0] for satir in imlec.fetchall()]
        bag.close()
        return modeller
    except Exception as e:
        print(f"Benzersiz modeller hatası: {e}")
        return []


def benzersiz_renkler(model):
    """Belirli bir modeldeki benzersiz renkleri döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "SELECT DISTINCT renk FROM stok WHERE model=? AND adet > 0 ORDER BY renk",
            (model,)
        )
        renkler = [satir[0] for satir in imlec.fetchall()]
        bag.close()
        return renkler
    except Exception as e:
        print(f"Benzersiz renkler hatası: {e}")
        return []


def mevcut_numaralar(model, renk):
    """Belirli model ve renkteki mevcut numaraları döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "SELECT numara, adet, fiyat FROM stok WHERE model=? AND renk=? AND adet > 0 ORDER BY numara",
            (model, renk)
        )
        numaralar = imlec.fetchall()
        bag.close()
        return numaralar
    except Exception as e:
        print(f"Mevcut numaralar hatası: {e}")
        return []


# GİDER İŞLEMLERİ

def gider_ekle(kategori, aciklama, tutar):
    """Yeni bir gider kaydı ekler."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "INSERT INTO giderler (kategori, aciklama, tutar) VALUES (?, ?, ?)",
            (kategori, aciklama, tutar)
        )
        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Gider ekleme hatası: {e}")
        return False


def tum_giderleri_getir():
    """Tüm gider kayıtlarını liste olarak döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT id, kategori, aciklama, tutar, tarih FROM giderler ORDER BY tarih DESC")
        giderler = imlec.fetchall()
        bag.close()
        return giderler
    except Exception as e:
        print(f"Gider getirme hatası: {e}")
        return []


def gider_sil(gider_id):
    """Belirtilen ID'ye sahip gider kaydını siler."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("DELETE FROM giderler WHERE id=?", (gider_id,))
        bag.commit()
        bag.close()
        return True
    except Exception as e:
        print(f"Gider silme hatası: {e}")
        return False


def toplam_gider():
    """Toplam gider tutarını döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute("SELECT COALESCE(SUM(tutar), 0) FROM giderler")
        sonuc = imlec.fetchone()[0]
        bag.close()
        return sonuc
    except Exception as e:
        print(f"Toplam gider hatası: {e}")
        return 0.0


def gunluk_gider():
    """Bugünkü toplam gider tutarını döndürür."""
    try:
        bag = baglanti_olustur()
        imlec = bag.cursor()
        imlec.execute(
            "SELECT COALESCE(SUM(tutar), 0) FROM giderler WHERE DATE(tarih) = DATE('now')"
        )
        sonuc = imlec.fetchone()[0]
        bag.close()
        return sonuc
    except Exception as e:
        print(f"Günlük gider hatası: {e}")
        return 0.0
