# Çaba Shoes – Satış Yapma Sayfası (sayfalar/satis.py)

import customtkinter as ctk
from tkinter import messagebox
from config import RENKLER
from database import (
    benzersiz_modeller, benzersiz_renkler, mevcut_numaralar,
    stok_bilgisi_getir, satis_kaydet
)


class SatisMixin:
    """Satış yapma sayfası metotlarını içeren mixin sınıfı."""

    def satis_goster(self):
        """Satış yapma sayfası – Ürün seçimi, indirim ve kayıt."""
        baslik = ctk.CTkLabel(
            self.icerik_alani, text="💰 Satış Yap",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=RENKLER["baslik"]
        )
        baslik.pack(anchor="w", padx=30, pady=(25, 15))

        satis_kart = ctk.CTkFrame(
            self.icerik_alani, fg_color=RENKLER["kart_bg"],
            corner_radius=14, border_width=1,
            border_color=RENKLER["kart_border"]
        )
        satis_kart.pack(padx=30, fill="x", pady=(0, 15))

        ctk.CTkLabel(
            satis_kart, text="🛒 Yeni Satış Kaydı",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=RENKLER["baslik"]
        ).pack(anchor="w", padx=20, pady=(15, 10))

        form = ctk.CTkFrame(satis_kart, fg_color="transparent")
        form.pack(padx=20, fill="x", pady=(0, 15))

        # Model seçimi (ComboBox)
        modeller = benzersiz_modeller()

        ctk.CTkLabel(form, text="Model", font=ctk.CTkFont(size=12),
                       text_color=RENKLER["metin_koyu"]).grid(row=0, column=0, padx=5, sticky="w")
        self.satis_model = ctk.CTkComboBox(
            form, values=modeller if modeller else ["Stok Boş"],
            height=38, corner_radius=8,
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8", button_color=RENKLER["buton_birincil"],
            command=self.satis_model_degisti
        )
        self.satis_model.grid(row=1, column=0, padx=5, sticky="ew")

        # Renk seçimi
        ctk.CTkLabel(form, text="Renk", font=ctk.CTkFont(size=12),
                       text_color=RENKLER["metin_koyu"]).grid(row=0, column=1, padx=5, sticky="w")
        self.satis_renk = ctk.CTkComboBox(
            form, values=["Önce model seçin"], height=38, corner_radius=8,
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8", button_color=RENKLER["buton_birincil"],
            command=self.satis_renk_degisti
        )
        self.satis_renk.grid(row=1, column=1, padx=5, sticky="ew")

        # Numara seçimi
        ctk.CTkLabel(form, text="Numara", font=ctk.CTkFont(size=12),
                       text_color=RENKLER["metin_koyu"]).grid(row=0, column=2, padx=5, sticky="w")
        self.satis_numara = ctk.CTkComboBox(
            form, values=["Önce renk seçin"], height=38, corner_radius=8,
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"],
            fg_color="#FDF2F8", button_color=RENKLER["buton_birincil"]
        )
        self.satis_numara.grid(row=1, column=2, padx=5, sticky="ew")

        # Adet
        ctk.CTkLabel(form, text="Adet", font=ctk.CTkFont(size=12),
                       text_color=RENKLER["metin_koyu"]).grid(row=0, column=3, padx=5, sticky="w")
        self.satis_adet = ctk.CTkEntry(
            form, height=38, corner_radius=8, placeholder_text="1",
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"], fg_color="#FDF2F8"
        )
        self.satis_adet.grid(row=1, column=3, padx=5, sticky="ew")

        # İndirim yüzdesi
        ctk.CTkLabel(form, text="İndirim (%)", font=ctk.CTkFont(size=12),
                       text_color=RENKLER["metin_koyu"]).grid(row=0, column=4, padx=5, sticky="w")
        self.satis_indirim = ctk.CTkEntry(
            form, height=38, corner_radius=8, placeholder_text="0",
            font=ctk.CTkFont(size=13),
            border_color=RENKLER["kenar_cubugu"], fg_color="#FDF2F8"
        )
        self.satis_indirim.grid(row=1, column=4, padx=5, sticky="ew")

        for i in range(5):
            form.grid_columnconfigure(i, weight=1)

        # Stok bilgi etiketi
        self.stok_bilgi = ctk.CTkLabel(
            satis_kart, text="", font=ctk.CTkFont(size=12),
            text_color=RENKLER["metin"]
        )
        self.stok_bilgi.pack(anchor="w", padx=25, pady=(0, 5))

        # Satış butonu
        ctk.CTkButton(
            satis_kart, text="💳  Satışı Kaydet", height=44,
            corner_radius=10, fg_color=RENKLER["basari"],
            hover_color="#059669",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.satis_kaydet_islem
        ).pack(padx=20, fill="x", pady=(5, 20))

        # Modeller varsa ilk modeli seç
        if modeller:
            self.satis_model.set(modeller[0])
            self.satis_model_degisti(modeller[0])

    def satis_model_degisti(self, secim):
        """Model seçildiğinde renk listesini günceller."""
        renkler = benzersiz_renkler(secim)
        if renkler:
            self.satis_renk.configure(values=renkler)
            self.satis_renk.set(renkler[0])
            self.satis_renk_degisti(renkler[0])
        else:
            self.satis_renk.configure(values=["Renk yok"])
            self.satis_renk.set("Renk yok")

    def satis_renk_degisti(self, secim):
        """Renk seçildiğinde numara listesini günceller."""
        model = self.satis_model.get()
        numaralar = mevcut_numaralar(model, secim)
        if numaralar:
            numara_listesi = [f"{n[0]} ({n[1]} adet - ₺{n[2]:,.0f})" for n in numaralar]
            self.satis_numara.configure(values=numara_listesi)
            self.satis_numara.set(numara_listesi[0])
            toplam_adet = sum(n[1] for n in numaralar)
            self.stok_bilgi.configure(text=f"ℹ️  {model} - {secim}: Toplam {toplam_adet} çift mevcut")
        else:
            self.satis_numara.configure(values=["Stokta yok"])
            self.satis_numara.set("Stokta yok")
            self.stok_bilgi.configure(text="⚠️ Bu kombinasyonda stok bulunmuyor")

    def satis_kaydet_islem(self):
        """Satış kaydını oluşturur."""
        try:
            model = self.satis_model.get()
            renk = self.satis_renk.get()
            numara_str = self.satis_numara.get()

            # Numarayı çıkart (örn: "37 (8 adet - ₺1,200)" → 37)
            numara = int(numara_str.split(" ")[0])
            adet = int(self.satis_adet.get().strip() or "1")
            indirim = float(self.satis_indirim.get().strip() or "0")

            # Doğrulama (koşul yapısı)
            if adet <= 0:
                messagebox.showwarning("Uyarı", "Adet sıfırdan büyük olmalıdır!")
                return
            if indirim < 0 or indirim > 100:
                messagebox.showwarning("Uyarı", "İndirim %0-%100 arası olmalıdır!")
                return

            # Fiyatı bul
            bilgi = stok_bilgisi_getir(model, renk, numara)
            if bilgi is None:
                messagebox.showerror("Hata", "Bu ürün stokta bulunamadı!")
                return

            birim_fiyat = bilgi[2]

            if satis_kaydet(model, renk, numara, adet, birim_fiyat, indirim):
                # İndirimli fiyat hesaplama (fonksiyon benzeri işlem)
                if indirim > 0:
                    toplam = birim_fiyat * adet * (1 - indirim / 100)
                    mesaj = f"✅ Satış kaydedildi!\n{model} {renk} {numara}\n{adet} adet × ₺{birim_fiyat:,.2f}\n%{indirim:.0f} indirim\nToplam: ₺{toplam:,.2f}"
                else:
                    toplam = birim_fiyat * adet
                    mesaj = f"✅ Satış kaydedildi!\n{model} {renk} {numara}\n{adet} adet × ₺{birim_fiyat:,.2f}\nToplam: ₺{toplam:,.2f}"

                messagebox.showinfo("Satış Başarılı", mesaj)
                # Formu yenile
                self.sayfa_degistir("satis")
            else:
                messagebox.showerror("Hata", "Stokta yeterli ürün yok veya bir hata oluştu!")

        except (ValueError, IndexError):
            messagebox.showerror("Hata", "Lütfen geçerli değerler girin!")
