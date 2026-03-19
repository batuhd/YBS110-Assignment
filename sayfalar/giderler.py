# Çaba Shoes – Gider Takibi Sayfası (sayfalar/giderler.py)

import customtkinter as ctk
from tkinter import messagebox, ttk
from config import RENKLER
from database import gider_ekle, tum_giderleri_getir, gider_sil, toplam_gider, gunluk_gider


class GiderlerMixin:
    """Gider takibi sayfası metotlarını içeren mixin sınıfı."""

    def giderler_goster(self):
        """Gider ekleme ve listeleme sayfası – gelir-gider takibi."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="💸 Gider Takibi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 15))

        # --- Gider Ekleme Formu ---
        form_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        form_kart.pack(padx=30, fill="x", pady=(0, 15))

        ctk.CTkLabel(
            form_kart, text="➕ Yeni Gider Ekle",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(anchor="w", padx=20, pady=(15, 10))

        girdi_frame = ctk.CTkFrame(form_kart, fg_color="transparent")
        girdi_frame.pack(padx=20, fill="x", pady=(0, 15))

        # Kategori seçimi
        ctk.CTkLabel(
            girdi_frame, text="Kategori",
            font=ctk.CTkFont(size=12),
            text_color=RENKLER["metin_koyu"]
        ).grid(row=0, column=0, padx=5, sticky="w")

        # Gider kategorileri listesi (list yapısı)
        gider_kategorileri = ["Kira", "Elektrik", "Su", "İnternet", "Maaş", "Malzeme", "Nakliye", "Reklam", "Bakım", "Diğer"]
        self.gider_kategori = ctk.CTkComboBox(
            girdi_frame, values=gider_kategorileri,
            height=38, corner_radius=8,
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8", button_color=RENKLER["buton_birincil"]
        )
        self.gider_kategori.grid(row=1, column=0, padx=5, sticky="ew")
        self.gider_kategori.set("Kira")

        # Açıklama
        ctk.CTkLabel(
            girdi_frame, text="Açıklama",
            font=ctk.CTkFont(size=12),
            text_color=RENKLER["metin_koyu"]
        ).grid(row=0, column=1, padx=5, sticky="w")

        self.gider_aciklama = ctk.CTkEntry(
            girdi_frame, height=38, corner_radius=8,
            placeholder_text="Gider açıklaması...",
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"], fg_color="#FDF2F8"
        )
        self.gider_aciklama.grid(row=1, column=1, padx=5, sticky="ew")

        # Tutar
        ctk.CTkLabel(
            girdi_frame, text="Tutar (₺)",
            font=ctk.CTkFont(size=12),
            text_color=RENKLER["metin_koyu"]
        ).grid(row=0, column=2, padx=5, sticky="w")

        self.gider_tutar = ctk.CTkEntry(
            girdi_frame, height=38, corner_radius=8,
            placeholder_text="0.00",
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"], fg_color="#FDF2F8"
        )
        self.gider_tutar.grid(row=1, column=2, padx=5, sticky="ew")

        # Ekle butonu
        ctk.CTkButton(
            girdi_frame, text="Ekle ✓", height=38, width=90,
            corner_radius=8, fg_color=RENKLER["basari"],
            hover_color="#059669",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.gider_ekle_islem
        ).grid(row=1, column=3, padx=(10, 0))

        for i in range(3):
            girdi_frame.grid_columnconfigure(i, weight=1)

        # --- Özet Kartları ---
        ozet_frame = ctk.CTkFrame(self.icerik_alani, fg_color="transparent")
        ozet_frame.pack(padx=30, fill="x", pady=(0, 10))

        t_gider = toplam_gider()
        g_gider = gunluk_gider()

        for i, (ikon, baslik_t, deger, renk) in enumerate([
            ("💸", "Toplam Gider", f"₺{t_gider:,.2f}", RENKLER["hata"]),
            ("📅", "Bugünkü Gider", f"₺{g_gider:,.2f}", RENKLER["uyari"]),
        ]):
            kart = ctk.CTkFrame(
                ozet_frame, fg_color=RENKLER["kart_bg"],
                corner_radius=14, border_width=1,
                border_color=RENKLER["kart_border"], height=90
            )
            kart.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            kart.grid_propagate(False)
            ozet_frame.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(kart, text=f"{ikon} {baslik_t}",
                         font=ctk.CTkFont(size=13),
                         text_color=RENKLER["metin"]).pack(pady=(15, 2))
            ctk.CTkLabel(kart, text=deger,
                         font=ctk.CTkFont(size=20, weight="bold"),
                         text_color=renk).pack()

        # --- Gider Tablosu ---
        tablo_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        tablo_kart.pack(padx=30, fill="both", expand=True, pady=(0, 15))

        ust_frame = ctk.CTkFrame(tablo_kart, fg_color="transparent")
        ust_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            ust_frame, text="📋 Gider Kayıtları",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(side="left")

        ctk.CTkButton(
            ust_frame, text="🗑 Seçileni Sil", height=34, width=120,
            corner_radius=8, fg_color=RENKLER["hata"],
            hover_color="#DC2626",
            font=ctk.CTkFont(size=12),
            command=self.gider_sil_islem
        ).pack(side="right")

        kolonlar = ("ID", "Kategori", "Açıklama", "Tutar", "Tarih")
        self.gider_tablo = ttk.Treeview(tablo_kart, columns=kolonlar, show="headings", height=8)

        for kol in kolonlar:
            self.gider_tablo.heading(kol, text=kol)
            self.gider_tablo.column(kol, width=120, anchor="center")

        self.gider_tablo.column("ID", width=50)
        self.gider_tablo.column("Açıklama", width=250)
        self.gider_tablo.column("Tarih", width=150)

        self.gider_tablo.pack(padx=20, fill="both", expand=True, pady=(0, 15))
        self.gider_tablosu_guncelle()

    def gider_ekle_islem(self):
        """Gider ekleme butonunun işlevi."""
        try:
            kategori = self.gider_kategori.get().strip()
            aciklama = self.gider_aciklama.get().strip()
            tutar = float(self.gider_tutar.get().strip())

            # Doğrulama (koşul yapısı)
            if not aciklama:
                messagebox.showwarning("Uyarı", "Açıklama alanı boş olamaz!")
                return
            if tutar <= 0:
                messagebox.showwarning("Uyarı", "Tutar sıfırdan büyük olmalıdır!")
                return

            if gider_ekle(kategori, aciklama, tutar):
                messagebox.showinfo("Başarılı", f"✅ Gider kaydedildi!\n{kategori}: {aciklama}\nTutar: ₺{tutar:,.2f}")
                self.gider_aciklama.delete(0, "end")
                self.gider_tutar.delete(0, "end")
                # Sayfayı yenile (özet kartlarını güncellemek için)
                self.sayfa_degistir("giderler")
            else:
                messagebox.showerror("Hata", "Gider kaydedilirken bir sorun oluştu!")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen tutar alanına geçerli bir sayı girin!")

    def gider_sil_islem(self):
        """Seçili gider kaydını siler."""
        secili = self.gider_tablo.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz gideri seçin!")
            return

        gider_id_val = self.gider_tablo.item(secili[0])["values"][0]
        if messagebox.askyesno("Onay", "Bu gider kaydını silmek istediğinize emin misiniz?"):
            if gider_sil(gider_id_val):
                messagebox.showinfo("Başarılı", "Gider kaydı silindi!")
                self.sayfa_degistir("giderler")

    def gider_tablosu_guncelle(self):
        """Gider tablosunu veritabanından güncel verilerle doldurur."""
        if hasattr(self, "gider_tablo"):
            for satir in self.gider_tablo.get_children():
                self.gider_tablo.delete(satir)

            # Döngü ile verileri tabloya ekle
            giderler = tum_giderleri_getir()
            for g in giderler:
                tutar_str = f"₺{g[3]:,.2f}"
                self.gider_tablo.insert("", "end", values=(g[0], g[1], g[2], tutar_str, g[4]))
