# Çaba Shoes – Satış Listesi Sayfası (sayfalar/satislar.py)

import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from config import RENKLER
from database import tum_satislari_getir


class SatislarMixin:
    """Satış listesi sayfası metotlarını içeren mixin sınıfı."""

    def satislar_goster(self):
        """Tüm satışları Pandas DataFrame ile listeler."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="📋 Satış Listesi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 15))

        # Pandas ile veri çekme
        satislar = tum_satislari_getir()

        if not satislar:
            ctk.CTkLabel(
                self.icerik_alani,
                text="📭  Henüz satış kaydı bulunmuyor.\nSatış yapmak için 💰 Satış Yap menüsünü kullanın.",
                font=ctk.CTkFont(size=14),
                text_color=RENKLER["metin"],
                justify="center"
            ).pack(expand=True)
            return

        # --- Pandas DataFrame oluşturma ---
        df = pd.DataFrame(satislar, columns=[
            "ID", "Model", "Renk", "Numara", "Adet",
            "Birim Fiyat", "İndirim %", "Toplam", "Tarih"
        ])

        # Özet bilgi kartı
        ozet_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        ozet_kart.pack(padx=30, fill="x", pady=(0, 10))

        ozet_frame = ctk.CTkFrame(ozet_kart, fg_color="transparent")
        ozet_frame.pack(padx=20, pady=12, fill="x")

        toplam_satis = int(df["Adet"].sum())
        toplam_ciro = float(df["Toplam"].sum())
        kayit_sayisi = len(df)

        ozet_bilgiler = [
            f"📊 {kayit_sayisi} satış kaydı",
            f"👟 {toplam_satis} adet satıldı",
            f"💰 ₺{toplam_ciro:,.2f} toplam ciro"
        ]

        for bilgi in ozet_bilgiler:
            ctk.CTkLabel(
                ozet_frame, text=bilgi,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=RENKLER["baslik"]
            ).pack(side="left", padx=15)

        # Satış tablosu
        tablo_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        tablo_kart.pack(padx=30, fill="both", expand=True, pady=(0, 15))

        kolonlar = ("ID", "Model", "Renk", "No", "Adet", "Birim ₺", "İndirim", "Toplam ₺", "Tarih")
        tablo = ttk.Treeview(tablo_kart, columns=kolonlar, show="headings", height=12)

        for kol in kolonlar:
            tablo.heading(kol, text=kol)
            tablo.column(kol, width=90, anchor="center")

        tablo.column("ID", width=40)
        tablo.column("Tarih", width=140)

        # DataFrame'den tabloya döngü ile veri aktar
        for _, satir in df.iterrows():
            tablo.insert("", "end", values=(
                satir["ID"], satir["Model"], satir["Renk"], satir["Numara"],
                satir["Adet"], f"₺{satir['Birim Fiyat']:,.2f}",
                f"%{satir['İndirim %']:.0f}", f"₺{satir['Toplam']:,.2f}",
                satir["Tarih"]
            ))

        tablo.pack(padx=20, fill="both", expand=True, pady=15)
