class Urun:
    def __init__(self,urun_adi,urun_fiyati,stok_miktari):
        self.urun_adi = urun_adi
        self.urun_fiyati = urun_fiyati
        self.stok_miktari = stok_miktari

class Yiyecek(Urun):
    def __init__(self, urun_adi, urun_fiyati, stok_miktari,porsiyon=1):
        super().__init__(urun_adi, urun_fiyati, stok_miktari)
        self.porsiyon = porsiyon

    def Bilgileri_goster(self):
        print(f"Ürün adı: {self.urun_adi}")
        print(f"Ürün fiyatı: {self.urun_fiyati} TL")
        print(f"Stok miktarı: {self.stok_miktari}")

class Icecek(Urun):
    def __init__(self, urun_adi, urun_fiyati, stok_miktari,boy):
        super().__init__(urun_adi, urun_fiyati, stok_miktari)
        self.boy = boy

    def Bilgileri_goster(self):
        print(f"Ürün adı : {self.urun_adi}")
        print(f"Ürün fiyatı: {self.urun_fiyati} TL")
        print(f"Stok miktarı: {self.stok_miktari}")
        print(f"İçecek boyu: {self.boy}")

Menu = []

sandivic = Yiyecek("Sandiviç",120,8,1)
tost = Yiyecek("tost",150,5,1)
pasta = Yiyecek("pasta",250,6,1)
kurabiye = Yiyecek("kurabiye",180,7,1)
Menu.extend([sandivic,tost,pasta,kurabiye])

kahve = Icecek("kahve",100,4,"tall")
cay = Icecek("çay",50,15,"small")
limonata = Icecek("limonata",80,8,"tall")
su = Icecek("su",10,15,"small")
Menu.extend([kahve,cay,limonata,su])

sepet = []
satislar = []

def siparis_olustur():
    while True:
        for sira, urun in enumerate(Menu, start=1):
            print(sira, urun.urun_adi)

        print("0. Sepeti görüntüle")
        print("9. Siparişi onayla")
        print("10. Siparişi iptal et")
        print("11. Rapor oluştur")

        try:
            secim = int(input("Ürün seçiniz: "))
        except ValueError:
            print("Lütfen sayısal bir değer giriniz!")
            continue

        if secim < 0 or (secim > len(Menu) and secim not in [9, 10, 11]):
            print("Geçersiz ürün numarası!")
            continue

        if secim == 0:
            ara_toplam = 0

            for siparis in sepet:
                urun = siparis[0]
                adet = siparis[1]
                tutar = urun.urun_fiyati * adet
                ara_toplam += tutar

                print(urun.urun_adi, "-", adet, "adet:", tutar, "TL")

            print("Ara toplam:", ara_toplam, "TL")

            if ara_toplam >= 500:
                indirim = ara_toplam * 0.10
                odenecek_tutar = ara_toplam - indirim
                print("İndirim:", indirim, "TL")
                print("İndirimli toplam:", odenecek_tutar, "TL")
            else:
                print("İndirim uygulanmadı.")
                print("Ödenecek toplam:", ara_toplam, "TL")

        if secim == 9:
            if len(sepet) == 0:
                print("Sepetiniz boş!")
                continue

            stok_yetersiz = False

            for siparis in sepet:
                urun = siparis[0]
                toplam_adet = sum(
                    s[1] for s in sepet if s[0] == urun
                )

                if toplam_adet > urun.stok_miktari:
                    print(urun.urun_adi, "için yeterli stok yok!")
                    stok_yetersiz = True

            if stok_yetersiz:
                continue

            ara_toplam = 0
            for siparis in sepet:
                urun = siparis[0]
                adet = siparis[1]
                ara_toplam += urun.urun_fiyati * adet

            print("Ara toplam:", ara_toplam, "TL")

            indirim = 0
            if ara_toplam >= 500:
                indirim = ara_toplam * 0.10

            odenecek_tutar = ara_toplam - indirim

            print("İndirim:", indirim, "TL")
            print("Ödenecek toplam:", odenecek_tutar, "TL")

            for siparis in sepet:
                urun = siparis[0]
                adet = siparis[1]
                urun.stok_miktari -= adet

            satislar.append({
                "tutar": odenecek_tutar,
                "urunler": [[siparis[0].urun_adi, siparis[1]] for siparis in sepet]
            })

            print("Siparişiniz onaylandı!")
            sepet.clear()

        if secim == 11:
            gunluk_rapor()
            continue

        if secim == 10:
            if len(sepet) == 0:
                print("İptal edilecek sipariş yok.")
            else:
                sepet.clear()
                print("Sipariş iptal edildi. Stoklar değişmedi.")
            continue

        for sira, urun in enumerate(Menu, start=1):
            if secim == sira:
                try:
                    adet = int(input("Kaç adet istiyorsunuz? "))
                except ValueError:
                    print("Lütfen adet için sayısal bir değer giriniz!")
                    continue

                if adet > urun.stok_miktari:
                    print("Yeterli stok yok!")
                elif adet <= 0:
                    print("Adet 1 veya daha fazla olmalıdır!")
                else:
                    sepet.append([urun, adet])
                    print(urun.urun_adi, "sepete eklendi.")

def gunluk_rapor():
    toplam_siparis = len(satislar)
    toplam_gelir = sum(satis["tutar"] for satis in satislar)
    urun_satislari = {}

    for satis in satislar:
        for urun_adi, adet in satis["urunler"]:
            urun_satislari[urun_adi] = urun_satislari.get(urun_adi, 0) + adet

    print("\n--- GÜNLÜK SATIŞ RAPORU ---")
    print("Toplam sipariş:", toplam_siparis)
    print("Toplam gelir:", toplam_gelir, "TL")

    if urun_satislari:
        en_cok_satilan = max(urun_satislari, key=urun_satislari.get)
        print("En çok satılan ürün:", en_cok_satilan)
        print("Satılan adet:", urun_satislari[en_cok_satilan])
    else:
        print("Henüz satış yapılmadı.")

siparis_olustur()












































