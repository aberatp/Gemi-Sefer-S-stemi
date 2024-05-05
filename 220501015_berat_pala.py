import pyodbc
import tkinter as tk
from tkinter import messagebox

class VeritabaniIslemleri:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                    'Server=BERATPALA\SQLEXPRESS;'
                                    'Database=veritabanı_adı;'
                                    'Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Gemiler')
                    BEGIN
                        CREATE TABLE Gemiler (
                            SeriNumarasi INT PRIMARY KEY,
                            Adi NVARCHAR(255),
                            Turu NVARCHAR(255),
                            Agirlik DECIMAL(18, 2),
                            YapimYili INT
                        )
                    END
                ''')
        self.conn.commit()
        self.cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Seferler')
                    BEGIN
                        CREATE TABLE Seferler (
                            ID INT PRIMARY KEY,
                            GemiSeriNumarasi INT,
                            YolaCikisTarihi DATE,
                            DonusTarihi DATE,
                            YolaCikisLimani NVARCHAR(255)
                        )
                    END
                ''')
        self.conn.commit()
        self.cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Kaptanlar')
                    BEGIN
                        CREATE TABLE Kaptanlar (
                            ID INT PRIMARY KEY,
                            Ad NVARCHAR(255),
                            Soyad NVARCHAR(255),
                            Adres NVARCHAR(255),
                            Vatandaslik NVARCHAR(255),
                            DogumTarihi DATE,
                            IsGirisTarihi DATE,
                            Lisans NVARCHAR(255),
                            SeferID INT
                        )
                    END
                ''')
        self.conn.commit()
        self.cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Murettebat')
                    BEGIN
                        CREATE TABLE Murettebat (
                            ID INT PRIMARY KEY,
                            Ad NVARCHAR(255),
                            Soyad NVARCHAR(255),
                            Adres NVARCHAR(255),
                            Vatandaslik NVARCHAR(255),
                            DogumTarihi DATE,
                            IsGirisTarihi DATE,
                            Gorev NVARCHAR(255),
                            SeferID INT
                        )
                    END
                ''')
        self.conn.commit()

    def gemi_ekle(self, seri_numarasi, adi, turu, agirlik, yapim_yili):
        self.cursor.execute("INSERT INTO Gemiler VALUES (?, ?, ?, ?, ?)",
                            (seri_numarasi, adi, turu, agirlik, yapim_yili))
        self.conn.commit()

    def sefer_ekle(self, ID, GemiSeriNumarasi, YolaCikisTarihi, DonusTarihi, YolaCikisLimani):
        self.cursor.execute("INSERT INTO Seferler VALUES (?, ?, ?, ?, ?)",
                            (ID, GemiSeriNumarasi, YolaCikisTarihi, DonusTarihi, YolaCikisLimani))
        self.conn.commit()

    def kaptan_ekle(self, ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Lisans, SeferID):
        self.cursor.execute("INSERT INTO Kaptanlar VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Lisans, SeferID))
        self.conn.commit()

    def murettebat_ekle(self, ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Gorev, SeferID):
        self.cursor.execute("INSERT INTO Murettebat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Gorev, SeferID))
        self.conn.commit()

    def close(self):
        self.conn.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gemiler Uygulaması")
        self.geometry("400x300")

        self.veritabani = VeritabaniIslemleri()

        self.label_gemi = tk.Label(self, text="Yeni Gemi Ekle")
        self.label_gemi.pack()

        self.frame_gemi = tk.Frame(self)
        self.frame_gemi.pack()

        self.seri_label = tk.Label(self.frame_gemi, text="Seri Numarası:")
        self.seri_label.grid(row=0, column=0)
        self.seri_entry = tk.Entry(self.frame_gemi)
        self.seri_entry.grid(row=0, column=1)

        self.adi_label = tk.Label(self.frame_gemi, text="Adı:")
        self.adi_label.grid(row=1, column=0)
        self.adi_entry = tk.Entry(self.frame_gemi)
        self.adi_entry.grid(row=1, column=1)

        self.turu_label = tk.Label(self.frame_gemi, text="Türü:")
        self.turu_label.grid(row=2, column=0)
        self.turu_entry = tk.Entry(self.frame_gemi)
        self.turu_entry.grid(row=2, column=1)

        self.agirlik_label = tk.Label(self.frame_gemi, text="Ağırlık:")
        self.agirlik_label.grid(row=3, column=0)
        self.agirlik_entry = tk.Entry(self.frame_gemi)
        self.agirlik_entry.grid(row=3, column=1)

        self.yapim_label = tk.Label(self.frame_gemi, text="Yapım Yılı:")
        self.yapim_label.grid(row=4, column=0)
        self.yapim_entry = tk.Entry(self.frame_gemi)
        self.yapim_entry.grid(row=4, column=1)

        self.ekle_gemi_button = tk.Button(self, text="Gemi Ekle", command=self.gemi_ekle)
        self.ekle_gemi_button.pack()

        self.label_sefer = tk.Label(self, text="Yeni Sefer Ekle")
        self.label_sefer.pack()

        self.frame_sefer = tk.Frame(self)
        self.frame_sefer.pack()

        self.sefer_ID_label = tk.Label(self.frame_sefer, text="Sefer ID:")
        self.sefer_ID_label.grid(row=0, column=0)
        self.sefer_ID_entry = tk.Entry(self.frame_sefer)
        self.sefer_ID_entry.grid(row=0, column=1)

        self.gemi_seri_label = tk.Label(self.frame_sefer, text="Gemi Seri Numarası:")
        self.gemi_seri_label.grid(row=1, column=0)
        self.gemi_seri_entry = tk.Entry(self.frame_sefer)
        self.gemi_seri_entry.grid(row=1, column=1)

        self.yola_cikis_label = tk.Label(self.frame_sefer, text="Yola Çıkış Tarihi:")
        self.yola_cikis_label.grid(row=2, column=0)
        self.yola_cikis_entry = tk.Entry(self.frame_sefer)
        self.yola_cikis_entry.grid(row=2, column=1)

        self.donus_label = tk.Label(self.frame_sefer, text="Dönüş Tarihi:")
        self.donus_label.grid(row=3, column=0)
        self.donus_entry = tk.Entry(self.frame_sefer)
        self.donus_entry.grid(row=3, column=1)

        self.yola_cikis_liman_label = tk.Label(self.frame_sefer, text="Yola Çıkış Limanı:")
        self.yola_cikis_liman_label.grid(row=4, column=0)
        self.yola_cikis_liman_entry = tk.Entry(self.frame_sefer)
        self.yola_cikis_liman_entry.grid(row=4, column=1)

        self.ekle_sefer_button = tk.Button(self, text="Sefer Ekle", command=self.sefer_ekle)
        self.ekle_sefer_button.pack()

        self.label_kaptan = tk.Label(self, text="Yeni Kaptan Ekle")
        self.label_kaptan.pack()

        self.frame_kaptan = tk.Frame(self)
        self.frame_kaptan.pack()

        self.kaptan_ID_label = tk.Label(self.frame_kaptan, text="Kaptan ID:")
        self.kaptan_ID_label.grid(row=0, column=0)
        self.kaptan_ID_entry = tk.Entry(self.frame_kaptan)
        self.kaptan_ID_entry.grid(row=0, column=1)

        self.ad_label = tk.Label(self.frame_kaptan, text="Ad:")
        self.ad_label.grid(row=1, column=0)
        self.ad_entry = tk.Entry(self.frame_kaptan)
        self.ad_entry.grid(row=1, column=1)

        self.soyad_label = tk.Label(self.frame_kaptan, text="Soyad:")
        self.soyad_label.grid(row=2, column=0)
        self.soyad_entry = tk.Entry(self.frame_kaptan)
        self.soyad_entry.grid(row=2, column=1)

        self.adres_label = tk.Label(self.frame_kaptan, text="Adres:")
        self.adres_label.grid(row=3, column=0)
        self.adres_entry = tk.Entry(self.frame_kaptan)
        self.adres_entry.grid(row=3, column=1)

        self.vatandaslik_label = tk.Label(self.frame_kaptan, text="Vatandaşlık:")
        self.vatandaslik_label.grid(row=4, column=0)
        self.vatandaslik_entry = tk.Entry(self.frame_kaptan)
        self.vatandaslik_entry.grid(row=4, column=1)

        self.dogum_label = tk.Label(self.frame_kaptan, text="Doğum Tarihi:")
        self.dogum_label.grid(row=5, column=0)
        self.dogum_entry = tk.Entry(self.frame_kaptan)
        self.dogum_entry.grid(row=5, column=1)

        self.is_giris_label = tk.Label(self.frame_kaptan, text="İşe Giriş Tarihi:")
        self.is_giris_label.grid(row=6, column=0)
        self.is_giris_entry = tk.Entry(self.frame_kaptan)
        self.is_giris_entry.grid(row=6, column=1)

        self.lisans_label = tk.Label(self.frame_kaptan, text="Lisans:")
        self.lisans_label.grid(row=7, column=0)
        self.lisans_entry = tk.Entry(self.frame_kaptan)
        self.lisans_entry.grid(row=7, column=1)

        self.kaptan_sefer_label = tk.Label(self.frame_kaptan, text="Sefer ID:")
        self.kaptan_sefer_label.grid(row=8, column=0)
        self.kaptan_sefer_entry = tk.Entry(self.frame_kaptan)
        self.kaptan_sefer_entry.grid(row=8, column=1)

        self.ekle_kaptan_button = tk.Button(self, text="Kaptan Ekle", command=self.kaptan_ekle)
        self.ekle_kaptan_button.pack()

        self.label_murettebat = tk.Label(self, text="Yeni Mürettebat Ekle")
        self.label_murettebat.pack()

        self.frame_murettebat = tk.Frame(self)
        self.frame_murettebat.pack()

        self.murettebat_ID_label = tk.Label(self.frame_murettebat, text="Mürettebat ID:")
        self.murettebat_ID_label.grid(row=0, column=0)
        self.murettebat_ID_entry = tk.Entry(self.frame_murettebat)
        self.murettebat_ID_entry.grid(row=0, column=1)

        self.m_ad_label = tk.Label(self.frame_murettebat, text="Ad:")
        self.m_ad_label.grid(row=1, column=0)
        self.m_ad_entry = tk.Entry(self.frame_murettebat)
        self.m_ad_entry.grid(row=1, column=1)

        self.m_soyad_label = tk.Label(self.frame_murettebat, text="Soyad:")
        self.m_soyad_label.grid(row=2, column=0)
        self.m_soyad_entry = tk.Entry(self.frame_murettebat)
        self.m_soyad_entry.grid(row=2, column=1)

        self.m_adres_label = tk.Label(self.frame_murettebat, text="Adres:")
        self.m_adres_label.grid(row=3, column=0)
        self.m_adres_entry = tk.Entry(self.frame_murettebat)
        self.m_adres_entry.grid(row=3, column=1)

        self.m_vatandaslik_label = tk.Label(self.frame_murettebat, text="Vatandaşlık:")
        self.m_vatandaslik_label.grid(row=4, column=0)
        self.m_vatandaslik_entry = tk.Entry(self.frame_murettebat)
        self.m_vatandaslik_entry.grid(row=4, column=1)

        self.m_dogum_label = tk.Label(self.frame_murettebat, text="Doğum Tarihi:")
        self.m_dogum_label.grid(row=5, column=0)
        self.m_dogum_entry = tk.Entry(self.frame_murettebat)
        self.m_dogum_entry.grid(row=5, column=1)

        self.m_is_giris_label = tk.Label(self.frame_murettebat, text="İşe Giriş Tarihi:")
        self.m_is_giris_label.grid(row=6, column=0)
        self.m_is_giris_entry = tk.Entry(self.frame_murettebat)
        self.m_is_giris_entry.grid(row=6, column=1)

        self.m_gorev_label = tk.Label(self.frame_murettebat, text="Görev:")
        self.m_gorev_label.grid(row=7, column=0)
        self.m_gorev_entry = tk.Entry(self.frame_murettebat)
        self.m_gorev_entry.grid(row=7, column=1)

        self.m_sefer_label = tk.Label(self.frame_murettebat, text="Sefer ID:")
        self.m_sefer_label.grid(row=8, column=0)
        self.m_sefer_entry = tk.Entry(self.frame_murettebat)
        self.m_sefer_entry.grid(row=8, column=1)

        self.ekle_murettebat_button = tk.Button(self, text="Mürettebat Ekle", command=self.murettebat_ekle)
        self.ekle_murettebat_button.pack()

    def gemi_ekle(self):
        seri_numarasi = self.seri_entry.get()
        adi = self.adi_entry.get()
        turu = self.turu_entry.get()
        agirlik = self.agirlik_entry.get()
        yapim_yili = self.yapim_entry.get()

        self.veritabani.gemi_ekle(seri_numarasi, adi, turu, agirlik, yapim_yili)
        messagebox.showinfo("Başarılı", "Yeni gemi başarıyla eklendi.")

    def sefer_ekle(self):
        ID = self.sefer_ID_entry.get()
        GemiSeriNumarasi = self.gemi_seri_entry.get()
        YolaCikisTarihi = self.yola_cikis_entry.get()
        DonusTarihi = self.donus_entry.get()
        YolaCikisLimani = self.yola_cikis_liman_entry.get()

        self.veritabani.sefer_ekle(ID, GemiSeriNumarasi, YolaCikisTarihi, DonusTarihi, YolaCikisLimani)
        messagebox.showinfo("Başarılı", "Yeni sefer başarıyla eklendi.")

    def kaptan_ekle(self):
        ID = self.kaptan_ID_entry.get()
        Ad = self.ad_entry.get()
        Soyad = self.soyad_entry.get()
        Adres = self.adres_entry.get()
        Vatandaslik = self.vatandaslik_entry.get()
        DogumTarihi = self.dogum_entry.get()
        IsGirisTarihi = self.is_giris_entry.get()
        Lisans = self.lisans_entry.get()
        SeferID = self.kaptan_sefer_entry.get()

        self.veritabani.kaptan_ekle(ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Lisans, SeferID)
        messagebox.showinfo("Başarılı", "Yeni kaptan başarıyla eklendi.")

    def murettebat_ekle(self):
        ID = self.murettebat_ID_entry.get()
        Ad = self.m_ad_entry.get()
        Soyad = self.m_soyad_entry.get()
        Adres = self.m_adres_entry.get()
        Vatandaslik = self.m_vatandaslik_entry.get()
        DogumTarihi = self.m_dogum_entry.get()
        IsGirisTarihi = self.m_is_giris_entry.get()
        Gorev = self.m_gorev_entry.get()
        SeferID = self.m_sefer_entry.get()

        self.veritabani.murettebat_ekle(ID, Ad, Soyad, Adres, Vatandaslik, DogumTarihi, IsGirisTarihi, Gorev, SeferID)
        messagebox.showinfo("Başarılı", "Yeni mürettebat başarıyla eklendi.")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()

