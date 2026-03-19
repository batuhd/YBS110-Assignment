# Çaba Shoes – Ana Uygulama (main.py)
# Kadın Ayakkabı Butiği Yönetim Sistemi
# Python Dersi Ödevi


import customtkinter as ctk
from tkinter import messagebox

# Kendi modüllerimiz
from config import RENKLER
from giris_ekrani import GirisEkrani
from database import tablolari_olustur
from auth import varsayilan_admin_olustur, demo_stok_yukle, demo_satis_yukle, demo_gider_yukle

# Sayfa mixin'leri (her sayfa ayrı dosyada)
from sayfalar.dashboard import DashboardMixin
from sayfalar.stok import StokMixin
from sayfalar.satis import SatisMixin
from sayfalar.satislar import SatislarMixin
from sayfalar.giderler import GiderlerMixin
from sayfalar.analiz import AnalizMixin


# ANA UYGULAMA – Sidebar Navigasyonlu Ana Pencere

class AnaUygulama(
    DashboardMixin,
    StokMixin,
    SatisMixin,
    SatislarMixin,
    GiderlerMixin,
    AnalizMixin,
    ctk.CTk
):
    """Ana uygulama penceresi – Dashboard, Stok, Satış, Analiz sekmeleri."""

    def __init__(self):
        super().__init__()

        self.title("👠 Çaba Shoes – Butik Yönetim Paneli")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.configure(fg_color=RENKLER["arkaplan"])

        # Aktif sayfa değişkeni
        self.aktif_sayfa = "dashboard"

        # --- Sol Kenar Çubuğu (Sidebar) ---
        self.sidebar = ctk.CTkFrame(
            self, width=220, fg_color=RENKLER["kart_bg"],
            corner_radius=0, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar logo
        ctk.CTkLabel(
            self.sidebar, text="👠 Çaba Shoes",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self.sidebar, text="Butik Yönetim Paneli",
            font=ctk.CTkFont(size=11),
            text_color=RENKLER["metin"]
        ).pack(pady=(0, 25))

        # Navigasyon butonları (liste yapısı ile oluşturma – döngü kullanımı)
        self.nav_butonlari = {}
        sayfa_listesi = [
            ("dashboard",  "📊  Dashboard"),
            ("stok",       "📦  Stok Yönetimi"),
            ("satis",      "💰  Satış Yap"),
            ("satislar",   "📋  Satış Listesi"),
            ("giderler",   "💸  Gider Takibi"),
            ("analiz",     "📈  Analiz"),
        ]

        # Döngü ile butonları oluştur (for loop kullanımı)
        for sayfa_id, etiket in sayfa_listesi:
            btn = ctk.CTkButton(
                self.sidebar, text=etiket, height=42,
                corner_radius=10, anchor="w",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color=RENKLER["metin_koyu"],
                hover_color=RENKLER["kenar_cubugu"],
                command=lambda sid=sayfa_id: self.sayfa_degistir(sid)
            )
            btn.pack(padx=12, pady=3, fill="x")
            self.nav_butonlari[sayfa_id] = btn

        # Çıkış butonu (altta)
        ctk.CTkButton(
            self.sidebar, text="🚪  Çıkış Yap", height=40,
            corner_radius=10, anchor="w",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color=RENKLER["hata"],
            hover_color="#FEE2E2",
            command=self.cikis_yap
        ).pack(side="bottom", padx=12, pady=15, fill="x")

        # --- Sağ İçerik Alanı ---
        self.icerik_alani = ctk.CTkFrame(self, fg_color=RENKLER["arkaplan"], corner_radius=0)
        self.icerik_alani.pack(side="right", fill="both", expand=True)

        # İlk sayfa: Dashboard
        self.sayfa_degistir("dashboard")

    def sayfa_degistir(self, sayfa_id):
        """Kenar çubuğundaki seçime göre sayfa değiştirir."""
        self.aktif_sayfa = sayfa_id

        # Buton renklerini güncelle (döngü + koşul)
        for sid, btn in self.nav_butonlari.items():
            if sid == sayfa_id:
                btn.configure(
                    fg_color=RENKLER["kenar_cubugu"],
                    text_color=RENKLER["kenar_aktif"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=RENKLER["metin_koyu"]
                )

        # İçerik alanını temizle
        for widget in self.icerik_alani.winfo_children():
            widget.destroy()

        # Sayfa yönlendirme (koşul yapısı)
        if sayfa_id == "dashboard":
            self.dashboard_goster()
        elif sayfa_id == "stok":
            self.stok_goster()
        elif sayfa_id == "satis":
            self.satis_goster()
        elif sayfa_id == "satislar":
            self.satislar_goster()
        elif sayfa_id == "giderler":
            self.giderler_goster()
        elif sayfa_id == "analiz":
            self.analiz_goster()

    # ÇIKIŞ
    def cikis_yap(self):
        """Uygulamadan çıkış yapar."""
        if messagebox.askyesno("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
            self.destroy()


# UYGULAMAYI BAŞLAT

if __name__ == "__main__":
    # Veritabanı ve tabloları oluştur
    tablolari_olustur()

    # Varsayılan admin hesabını oluştur
    varsayilan_admin_olustur()

    # Demo verileri yükle (stok, satış, gider)
    demo_stok_yukle()
    demo_satis_yukle()
    demo_gider_yukle()

    # Giriş ekranını başlat
    giris = GirisEkrani(AnaUygulama)
    giris.mainloop()
