# Çaba Shoes – Dashboard Sayfası (sayfalar/dashboard.py)

import customtkinter as ctk
from config import RENKLER
from database import toplam_stok_sayisi, toplam_model_sayisi, gunluk_satis_ozeti


class DashboardMixin:
    """Dashboard sayfası metotlarını içeren mixin sınıfı."""

    def dashboard_goster(self):
        """Ana pano – Toplam stok, model sayısı ve günlük satış özeti."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="📊 Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            self.icerik_alani, text="Çaba Shoes butik yönetim özetiniz",
            font=ctk.CTkFont(size=13),
            text_color=RENKLER["metin"]
        ).pack(anchor="w", padx=30, pady=(0, 20))

        # Verileri çek
        t_stok = toplam_stok_sayisi()
        t_model = toplam_model_sayisi()
        g_adet, g_ciro = gunluk_satis_ozeti()

        # Kartlar (liste + döngü ile oluştur)
        kart_frame = ctk.CTkFrame(self.icerik_alani, fg_color="transparent")
        kart_frame.pack(padx=30, fill="x")

        kart_verileri = [
            ("📦", "Toplam Stok", str(t_stok), "çift ayakkabı", RENKLER["buton_birincil"]),
            ("👟", "Model Çeşidi", str(t_model), "farklı model", RENKLER["basari"]),
            ("🛒", "Bugünkü Satış", str(g_adet), "adet satıldı", RENKLER["uyari"]),
            ("💰", "Bugünkü Ciro", f"₺{g_ciro:,.2f}", "toplam gelir", RENKLER["kenar_aktif"]),
        ]

        for i, (ikon, baslik_t, deger, alt_t, renk) in enumerate(kart_verileri):
            kart = ctk.CTkFrame(
                kart_frame, fg_color=RENKLER["kart_bg"],
                corner_radius=14, border_width=1,
                border_color=RENKLER["kart_border"], height=140
            )
            kart.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            kart.grid_propagate(False)
            kart_frame.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(kart, text=ikon, font=ctk.CTkFont(size=30)).pack(pady=(18, 2))
            ctk.CTkLabel(
                kart, text=baslik_t,
                font=ctk.CTkFont(size=12),
                text_color=RENKLER["metin"]
            ).pack()
            ctk.CTkLabel(
                kart, text=deger,
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=renk
            ).pack()
            ctk.CTkLabel(
                kart, text=alt_t,
                font=ctk.CTkFont(size=11),
                text_color=RENKLER["metin"]
            ).pack()

        # --- Hızlı Erişim Butonları ---
        hizli_frame = ctk.CTkFrame(self.icerik_alani, fg_color="transparent")
        hizli_frame.pack(padx=30, pady=20, fill="x")

        ctk.CTkLabel(
            hizli_frame, text="⚡ Hızlı İşlemler",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(anchor="w", pady=(0, 10))

        btn_frame = ctk.CTkFrame(hizli_frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        ctk.CTkButton(
            btn_frame, text="📦 Stok Ekle", height=44,
            corner_radius=10, fg_color=RENKLER["buton_birincil"],
            hover_color=RENKLER["buton_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.sayfa_degistir("stok")
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="💰 Satış Yap", height=44,
            corner_radius=10, fg_color=RENKLER["basari"],
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.sayfa_degistir("satis")
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="📈 Analiz Göster", height=44,
            corner_radius=10, fg_color=RENKLER["uyari"],
            hover_color="#D97706",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.sayfa_degistir("analiz")
        ).pack(side="left")
