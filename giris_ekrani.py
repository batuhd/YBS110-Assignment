# Çaba Shoes – Giriş (Login) Ekranı (giris_ekrani.py)

import customtkinter as ctk
from config import RENKLER
from auth import giris_dogrula


class GirisEkrani(ctk.CTk):
    """Admin giriş penceresi – SHA-256 ile şifre doğrulama."""

    def __init__(self, uygulama_sinifi):
        super().__init__()

        # Ana uygulama sınıfını sakla (giriş sonrası açmak için)
        self.uygulama_sinifi = uygulama_sinifi

        # Pencere ayarları
        self.title("👠 Çaba Shoes – Giriş")
        self.geometry("480x580")
        self.resizable(False, False)
        self.configure(fg_color=RENKLER["arkaplan"])

        # --- Logo / Başlık Alanı ---
        baslik_frame = ctk.CTkFrame(self, fg_color="transparent")
        baslik_frame.pack(pady=(60, 10))

        # Ayakkabı emojisi ile logo
        ctk.CTkLabel(
            baslik_frame, text="👠",
            font=ctk.CTkFont(size=64)
        ).pack()

        ctk.CTkLabel(
            baslik_frame, text="Çaba Shoes",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(pady=(5, 0))

        ctk.CTkLabel(
            baslik_frame, text="Butik Yönetim Sistemi",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=RENKLER["metin"]
        ).pack()

        # --- Giriş Formu ---
        form_frame = ctk.CTkFrame(
            self, fg_color=RENKLER["kart_bg"],
            corner_radius=16, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        form_frame.pack(padx=50, pady=30, fill="x")

        ctk.CTkLabel(
            form_frame, text="Yönetici Girişi",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(pady=(25, 15))

        # Kullanıcı adı
        ctk.CTkLabel(
            form_frame, text="Kullanıcı Adı",
            font=ctk.CTkFont(size=13),
            text_color=RENKLER["metin_koyu"],
            anchor="w"
        ).pack(padx=30, anchor="w")

        self.kullanici_entry = ctk.CTkEntry(
            form_frame, height=42, corner_radius=10,
            placeholder_text="admin",
            font=ctk.CTkFont(size=14),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8"
        )
        self.kullanici_entry.pack(padx=30, fill="x", pady=(4, 12))

        # Şifre
        ctk.CTkLabel(
            form_frame, text="Şifre",
            font=ctk.CTkFont(size=13),
            text_color=RENKLER["metin_koyu"],
            anchor="w"
        ).pack(padx=30, anchor="w")

        self.sifre_entry = ctk.CTkEntry(
            form_frame, height=42, corner_radius=10,
            placeholder_text="••••••",
            show="•", font=ctk.CTkFont(size=14),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8"
        )
        self.sifre_entry.pack(padx=30, fill="x", pady=(4, 20))

        # Giriş butonu
        self.giris_btn = ctk.CTkButton(
            form_frame, text="Giriş Yap", height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=RENKLER["buton_birincil"],
            hover_color=RENKLER["buton_hover"],
            command=self.giris_yap
        )
        self.giris_btn.pack(padx=30, fill="x", pady=(0, 25))

        # Enter tuşu ile giriş
        self.bind("<Return>", lambda e: self.giris_yap())

        # Hata mesajı etiketi (başlangıçta gizli)
        self.hata_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12),
            text_color=RENKLER["hata"]
        )
        self.hata_label.pack()

        # Bilgi notu
        ctk.CTkLabel(
            self, text="Varsayılan: admin / sifre123",
            font=ctk.CTkFont(size=11),
            text_color=RENKLER["metin"]
        ).pack(side="bottom", pady=15)

    def giris_yap(self):
        """Giriş butonuna basıldığında çalışır."""
        kullanici = self.kullanici_entry.get().strip()
        sifre = self.sifre_entry.get().strip()

        # Boş alan kontrolü (koşul yapısı)
        if not kullanici or not sifre:
            self.hata_label.configure(text="⚠️ Lütfen tüm alanları doldurun!")
            return

        # SHA-256 ile doğrulama (auth modülünden)
        if giris_dogrula(kullanici, sifre):
            self.destroy()  # Giriş ekranını kapat
            uygulama = self.uygulama_sinifi()  # Ana uygulamayı aç
            uygulama.mainloop()
        else:
            self.hata_label.configure(text="❌ Hatalı kullanıcı adı veya şifre!")
            self.sifre_entry.delete(0, "end")
