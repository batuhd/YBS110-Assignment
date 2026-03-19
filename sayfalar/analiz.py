# Çaba Shoes – Analiz Sayfası (sayfalar/analiz.py)

import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")  # Tkinter ile uyumlu backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import RENKLER
from database import model_bazli_satis, tum_satislari_getir, toplam_gider


class AnalizMixin:
    """Analiz sayfası metotlarını içeren mixin sınıfı."""

    def analiz_goster(self):
        """Model bazlı satış analiz grafiği – Matplotlib bar chart."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="📈 Satış Analizi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 15))

        # Verileri çek (sözlük yapısı)
        satis_verileri = model_bazli_satis()

        if not satis_verileri:
            ctk.CTkLabel(
                self.icerik_alani,
                text="📭  Henüz analiz edilecek satış verisi yok.\nSatış yapıldıkça grafikler burada görünecek.",
                font=ctk.CTkFont(size=14),
                text_color=RENKLER["metin"],
                justify="center"
            ).pack(expand=True)
            return

        # --- KÂR-ZARAR ÖZET KARTLARI ---
        # Toplam gelir (satışlardan) ve toplam gider hesaplama
        satislar = tum_satislari_getir()
        toplam_gelir = sum(s[7] for s in satislar)  # toplam_fiyat sütunu
        toplam_gid = toplam_gider()

        # Net kâr/zarar hesaplama (koşul yapısı)
        net_kar = toplam_gelir - toplam_gid
        if toplam_gelir > 0:
            kar_marji = (net_kar / toplam_gelir) * 100
        else:
            kar_marji = 0.0

        # Kâr mı zarar mı? (koşul yapısı)
        if net_kar >= 0:
            kar_renk = RENKLER["basari"]
            kar_ikon = "📈"
            kar_durum = "KÂR"
        else:
            kar_renk = RENKLER["hata"]
            kar_ikon = "📉"
            kar_durum = "ZARAR"

        kz_frame = ctk.CTkFrame(self.icerik_alani, fg_color="transparent")
        kz_frame.pack(padx=30, fill="x", pady=(0, 12))

        kz_verileri = [
            ("💰", "Toplam Gelir", f"₺{toplam_gelir:,.2f}", RENKLER["basari"]),
            ("💸", "Toplam Gider", f"₺{toplam_gid:,.2f}", RENKLER["hata"]),
            (kar_ikon, f"Net {kar_durum}", f"₺{abs(net_kar):,.2f}", kar_renk),
            ("📊", "Kâr Marjı", f"%{kar_marji:.1f}", kar_renk),
        ]

        # Döngü ile kâr-zarar kartlarını oluştur
        for i, (ikon, baslik_t, deger, renk) in enumerate(kz_verileri):
            kart = ctk.CTkFrame(
                kz_frame, fg_color=RENKLER["kart_bg"],
                corner_radius=14, border_width=1,
                border_color=RENKLER["kart_border"], height=100
            )
            kart.grid(row=0, column=i, padx=6, pady=5, sticky="nsew")
            kart.grid_propagate(False)
            kz_frame.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(kart, text=f"{ikon} {baslik_t}",
                         font=ctk.CTkFont(size=12),
                         text_color=RENKLER["metin"]).pack(pady=(14, 2))
            ctk.CTkLabel(kart, text=deger,
                         font=ctk.CTkFont(size=20, weight="bold"),
                         text_color=renk).pack()

        grafik_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        grafik_kart.pack(padx=30, fill="both", expand=True, pady=(0, 15))

        ctk.CTkLabel(
            grafik_kart, text="📊 Model Bazlı Satış Grafiği",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # --- Matplotlib grafiği oluşturma ---
        modeller_listesi = list(satis_verileri.keys())
        adetler = list(satis_verileri.values())

        # Renk paleti (pembe tonları – butik temasına uygun)
        pembe_tonlari = ["#EC4899", "#F472B6", "#FBCFE8", "#F9A8D4",
                          "#DB2777", "#BE185D", "#9D174D", "#831843"]
        bar_renkleri = [pembe_tonlari[i % len(pembe_tonlari)] for i in range(len(modeller_listesi))]

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FDF2F8")

        barlar = ax.bar(modeller_listesi, adetler, color=bar_renkleri,
                         edgecolor="#FFFFFF", linewidth=1.5)

        # Bar üzerine değer yazma (döngü)
        for bar, deger in zip(barlar, adetler):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    str(deger), ha="center", va="bottom",
                    fontsize=12, fontweight="bold", color="#831843")

        ax.set_xlabel("Ayakkabı Modeli", fontsize=12, color="#6B7280", labelpad=10)
        ax.set_ylabel("Satış Adedi", fontsize=12, color="#6B7280", labelpad=10)
        ax.set_title("Çaba Shoes – Model Bazlı Satışlar", fontsize=14,
                      fontweight="bold", color="#831843", pad=15)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E5E7EB")
        ax.spines["bottom"].set_color("#E5E7EB")
        ax.tick_params(colors="#6B7280")

        plt.tight_layout()

        # Canvas ile Tkinter'a entegre et
        canvas = FigureCanvasTkAgg(fig, master=grafik_kart)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=20, fill="both", expand=True, pady=(5, 15))

        # Ayrı pencerede açma butonu
        ctk.CTkButton(
            grafik_kart, text="🔍  Grafiği Büyük Pencerede Aç", height=40,
            corner_radius=10, fg_color=RENKLER["buton_birincil"],
            hover_color=RENKLER["buton_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self.grafik_ayri_pencere(satis_verileri)
        ).pack(padx=20, pady=(0, 15))

    def grafik_ayri_pencere(self, satis_verileri):
        """Matplotlib grafiğini ayrı bir pencerede açar (libs.md isteği)."""
        modeller_listesi = list(satis_verileri.keys())
        adetler = list(satis_verileri.values())

        pembe_tonlari = ["#EC4899", "#F472B6", "#FBCFE8", "#F9A8D4",
                          "#DB2777", "#BE185D", "#9D174D", "#831843"]
        bar_renkleri = [pembe_tonlari[i % len(pembe_tonlari)] for i in range(len(modeller_listesi))]

        plt.figure(figsize=(10, 6))
        plt.gcf().patch.set_facecolor("#FDF2F8")

        barlar = plt.bar(modeller_listesi, adetler, color=bar_renkleri,
                          edgecolor="#FFFFFF", linewidth=2)

        for bar, deger in zip(barlar, adetler):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                     str(deger), ha="center", va="bottom",
                     fontsize=13, fontweight="bold", color="#831843")

        plt.xlabel("Ayakkabı Modeli", fontsize=13, color="#6B7280")
        plt.ylabel("Satış Adedi", fontsize=13, color="#6B7280")
        plt.title("👠 Çaba Shoes – Satış Analiz Raporu", fontsize=16,
                   fontweight="bold", color="#831843")
        plt.tight_layout()
        plt.show()
