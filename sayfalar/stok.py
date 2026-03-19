# Çaba Shoes – Stok Yönetimi Sayfası (sayfalar/stok.py)

import customtkinter as ctk
from tkinter import messagebox, ttk
from config import RENKLER
from database import tum_stoklari_getir, stok_ekle, stok_sil


class StokMixin:
    """Stok yönetimi sayfası metotlarını içeren mixin sınıfı."""

    def stok_goster(self):
        """Stok yönetim sayfası – Ürün ekleme, listeleme ve silme."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="📦 Stok Yönetimi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 15))

        # --- Ürün Ekleme Formu ---
        form_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        form_kart.pack(padx=30, fill="x", pady=(0, 15))

        ctk.CTkLabel(
            form_kart, text="➕ Yeni Ürün Ekle",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(anchor="w", padx=20, pady=(15, 10))

        girdi_frame = ctk.CTkFrame(form_kart, fg_color="transparent")
        girdi_frame.pack(padx=20, fill="x", pady=(0, 15))

        # Girdi alanları (değişkenler)
        etiketler = ["Model", "Renk", "Numara (36-40)", "Adet", "Fiyat (₺)"]
        self.stok_girdiler = {}

        for i, etiket in enumerate(etiketler):
            ctk.CTkLabel(
                girdi_frame, text=etiket,
                font=ctk.CTkFont(size=12),
                text_color=RENKLER["metin_koyu"]
            ).grid(row=0, column=i, padx=5, pady=(0, 3), sticky="w")

            entry = ctk.CTkEntry(
                girdi_frame, height=38, corner_radius=8,
                border_color=RENKLER["kenar_cubugu"],
                fg_color="#FDF2F8", font=ctk.CTkFont(size=13)
            )
            entry.grid(row=1, column=i, padx=5, sticky="ew")
            girdi_frame.grid_columnconfigure(i, weight=1)
            self.stok_girdiler[etiket] = entry

        ctk.CTkButton(
            girdi_frame, text="Ekle ✓", height=38, width=90,
            corner_radius=8, fg_color=RENKLER["basari"],
            hover_color="#059669",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.stok_ekle_islem
        ).grid(row=1, column=len(etiketler), padx=(10, 0))

        # --- Stok Tablosu ---
        tablo_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        tablo_kart.pack(padx=30, fill="both", expand=True, pady=(0, 15))

        ust_frame = ctk.CTkFrame(tablo_kart, fg_color="transparent")
        ust_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            ust_frame, text="📋 Mevcut Stok",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(side="left")

        ctk.CTkButton(
            ust_frame, text="🗑 Seçileni Sil", height=34, width=120,
            corner_radius=8, fg_color=RENKLER["hata"],
            hover_color="#DC2626",
            font=ctk.CTkFont(size=12),
            command=self.stok_sil_islem
        ).pack(side="right")

        # Treeview tablosu (tkinter ttk)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 11),
                         background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"),
                         background=RENKLER["kenar_cubugu"], foreground=RENKLER["baslik"])
        style.map("Treeview", background=[("selected", RENKLER["kenar_cubugu"])])

        kolonlar = ("ID", "Model", "Renk", "Numara", "Adet", "Fiyat")
        self.stok_tablo = ttk.Treeview(tablo_kart, columns=kolonlar, show="headings", height=10)

        for kol in kolonlar:
            self.stok_tablo.heading(kol, text=kol)
            self.stok_tablo.column(kol, width=100, anchor="center")

        self.stok_tablo.column("ID", width=50)
        self.stok_tablo.column("Fiyat", width=120)

        self.stok_tablo.pack(padx=20, fill="both", expand=True, pady=(0, 15))
        self.stok_tablosu_guncelle()

    def stok_ekle_islem(self):
        """Stok ekleme butonunun işlevi."""
        try:
            model = self.stok_girdiler["Model"].get().strip()
            renk = self.stok_girdiler["Renk"].get().strip()
            numara = int(self.stok_girdiler["Numara (36-40)"].get().strip())
            adet = int(self.stok_girdiler["Adet"].get().strip())
            fiyat = float(self.stok_girdiler["Fiyat (₺)"].get().strip())

            # Doğrulama (koşul yapısı + try-except)
            if not model or not renk:
                messagebox.showwarning("Uyarı", "Model ve renk alanları boş olamaz!")
                return
            if numara < 36 or numara > 40:
                messagebox.showwarning("Uyarı", "Numara 36-40 arası olmalıdır!")
                return
            if adet <= 0 or fiyat <= 0:
                messagebox.showwarning("Uyarı", "Adet ve fiyat sıfırdan büyük olmalıdır!")
                return

            if stok_ekle(model, renk, numara, adet, fiyat):
                messagebox.showinfo("Başarılı", f"✅ {model} ({renk}, {numara}) stoka eklendi!")
                # Girdi alanlarını temizle (döngü)
                for entry in self.stok_girdiler.values():
                    entry.delete(0, "end")
                self.stok_tablosu_guncelle()
            else:
                messagebox.showerror("Hata", "Stok eklenirken bir sorun oluştu!")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen numara, adet ve fiyat alanlarına sayı girin!")

    def stok_sil_islem(self):
        """Seçili stok kaydını siler."""
        secili = self.stok_tablo.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz ürünü seçin!")
            return

        stok_id = self.stok_tablo.item(secili[0])["values"][0]
        if messagebox.askyesno("Onay", "Bu ürünü silmek istediğinize emin misiniz?"):
            if stok_sil(stok_id):
                messagebox.showinfo("Başarılı", "Ürün stoktan silindi!")
                self.stok_tablosu_guncelle()

    def stok_tablosu_guncelle(self):
        """Stok tablosunu veritabanından güncel verilerle doldurur."""
        if hasattr(self, "stok_tablo"):
            # Tabloyu temizle
            for satir in self.stok_tablo.get_children():
                self.stok_tablo.delete(satir)

            # Verileri çek ve tabloya ekle (döngü)
            stoklar = tum_stoklari_getir()
            for stok in stoklar:
                fiyat_str = f"₺{stok[5]:,.2f}"
                self.stok_tablo.insert("", "end", values=(stok[0], stok[1], stok[2], stok[3], stok[4], fiyat_str))
