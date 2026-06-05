# ===========================================
# ===SİNEMA BİLET VE SALON YÖNETİM SİSTEMİ===
# ===========================================

import datetime
import pickle

class Film:
    """Sistemdeki her bir filmin bilgilerini tanımlayan sınıf."""
    def __init__(self, film_id, film_adi, yonetmen, sure, tur):
        # Yeni bir film nesnesi oluşturulurken gerekli parametreleri atar.  
        self.__film_id = film_id
        self.film_adi = film_adi
        self.yonetmen = yonetmen
        self.sure = sure
        self.tur = tur

    @property
    def film_id(self):
        #Dışarıdan film ID'sinin değiştirilmesini önler, sadece okunmasını sağlar.
        return self.__film_id

# Sisteme rastgele veya hatalı film türleri girilmesini önlemek amacıyla,
# kabul edeceğimiz tüm geçerli film türlerini bir liste altında sabitledik.
GECERLI_TURLER = ["Aile", "Aksiyon", "Animasyon", "Belgesel", "Biyografi", "Bilim Kurgu", "Deneysel", "Doğaüstü", "Dram", "Dini", "Dövüş", "Fantastik", "Felsefi", "Gerilim", "Gençlik", "Gizem", "Hayatta Kalma", "Komedi", "Korku", "Macera", "Müzik", "Polisiye", "Politik", "Psikolojik", "Romantik", "Savaş", "Spor", "Suç", "Tarihî", "Trajedi"]

class Salon:
    """Salon bilgilerini ve koltuk kapasitelerini tanımlayan sınıf."""
    def __init__(self, salon_adi, kapasite):
        # Yeni bir salon oluşturulurken isim ve koltuk kapasitesi bilgilerini atar.
        self.salon_adi = salon_adi
        self.kapasite = kapasite

class Seans:
    """Hangi filmin, hangi salonda ve ne zaman oynatılacağını belirleyen sınıf."""
    def __init__(self, film, salon, saat):
        #Yeni bir seans planı oluşturur.
        self.film = film
        self.salon = salon
        self.saat = saat

class Koltuk(Seans):
    """Salonun koltuk düzenini ve doluluk durumlarını takip eden sınıf."""
    def __init__(self, film, salon, saat):
        #Seans bilgilerini miras alır ve salona özel koltuk şemasını hazırlar.
        Seans.__init__(self, film, salon, saat)

        self.__koltuklar = {}
        self.__koltuklari_hazirla()

    @property
    def koltuklar(self):
        # Koltuk düzenine dışarıdan sadece okuma amaçlı erişim sağlar.
        return self.__koltuklar

    def __koltuklari_hazirla(self):
        """Salonun kapasitesine göre harf sırası ve koltuk numaralarını otomatik oluşturur."""
        alfabe = "ABCDEFGHIJKLMNOPRSTUVYZ"
        
        # Her sırada 10 koltuk olacağı varsayımıyla toplam sıra sayısını hesaplar.
        toplam_sira = self.salon.kapasite // 10
        
        # Kapasite 10'un tam katı değilse kalan koltuklar için bir sıra daha ekler.
        if self.salon.kapasite % 10 != 0:
            toplam_sira += 1

        # Hesaplanan sıra sayısı kadar harf ataması yapar ve her sıraya 10 adet boş koltuk ekler.
        for i in range(toplam_sira):
            if i < len(alfabe):
                sira_harfi = alfabe[i]
                self.__koltuklar[sira_harfi] = {}
                
                for numara in range(1, 11):
                    self.__koltuklar[sira_harfi][numara] = False

    def koltuk_durumu_goster(self):
        """Salonun anlık doluluk planını ekrana görsel olarak basar."""
        print(f"\n--- {self.salon.salon_adi} | Saat: {self.saat} Koltuk Durumu ---\n")
        print("   1  2  3  4  5  6  7  8  9  10")
        print("  ---------------------------------")
            
        for sira, numaralar in self.__koltuklar.items():
            satir = f"{sira} | "
            for numara in range(1, 11):
                if numaralar[numara] != False:
                    satir += "X  "   
                else:
                    satir += "O  "   
            print(satir)
            
        print("  ---------------------------------")
        print("PERDE (O: Boş, X: Dolu)\n")

class Bilet:
    """Satılan her bir biletin tür, fiyat ve konum bilgilerini tutan sınıf."""
    def __init__(self, bilet_tipi, fiyat, sira, numara):
        # Bilet bilgilerini alır ve sonradan değiştirilmemesi için gizli kaydeder.
        self.__bilet_tipi = bilet_tipi
        self.__fiyat = fiyat
        self.__sira = sira
        self.__numara = numara
    
    # Bilet bilgilerinin dışarıdan sadece okunmasını sağlar.
    @property
    def bilet_tipi(self):
        return self.__bilet_tipi
    @property
    def fiyat(self):
        return self.__fiyat
    @property
    def sira(self):
        return self.__sira
    @property
    def numara(self):
        return self.__numara

class SinemaSistemi:
    """Tüm sinema operasyonlarını, kayıtları ve finansal durumu yöneten ana sınıf."""
    def __init__(self):
        # Eklenen filmleri, salonları, seansları ve toplam geliri takip etmek için ilk değerleri atar.
        self.__filmler = []
        self.__salonlar = []
        self.__seanslar = []
        self.__toplam_gelir = 0

    # Listelerin dışarıdan sadece okunmasını sağlar.
    @property
    def filmler(self):
        return self.__filmler
    @property
    def salonlar(self):
        return self.__salonlar
    @property
    def seanslar(self):
        return self.__seanslar
    @property
    def toplam_gelir(self):
        return self.__toplam_gelir

    # -----------------------
    # -------FİLM EKLE-------
    # -----------------------
    def film_ekle(self):
        """Kullanıcıdan terminal yoluyla film bilgilerini aldığımız ve listemize kaydettiğimiz fonksiyon."""
        print("\n--- YENİ FİLM EKLEME PANELİ ---")
        
        # Film adı girişi ve boş değer/iptal kontrolü döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            film_adi = input("Film Adı: ").strip()

            if film_adi == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            elif film_adi:
                break
            else:
                print("Hata: Lütfen bu alanı boş bırakmayınız.")
                continue

        # Yönetmen ismi girişi ve doğrulama döngüsü. 
        while True:
            yonetmen = input("Yönetmen: ").strip()

            if yonetmen == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            elif yonetmen:
                break
            else:
                print("Hata: Lütfen bu alanı boş bırakmayınız.")
                continue
            
        # Süre kısmında kullanıcının harf veya geçersiz karakter girmesi durumunda,
        # veri girişi döngüye alınarak try-except bloklarıyla kontrol edilir.
        while True:
            sure_input = input("Süre (Dakika): ").strip()

            if sure_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not sure_input:
                print("Hata: Lütfen bu alanı boş bırakmayınız.")
                continue

            # Girdi içerisindeki harf ve eksi (-) dahil tüm özel karakterleri temizler.
            # Sadece sayısal (0-9) karakterleri birleştirerek temiz bir metin verisi elde eder.
            temiz_sure_metni = "".join([karakter for karakter in sure_input if karakter.isdigit()])
            
            try:
                sure = int(temiz_sure_metni)
                break
            except ValueError:
                print("Hata: Süre alanına sadece sayısal bir değer girebilirsiniz!")
        
        # Film türü girişi ve çoklu tür doğrulama döngüsü.
        while True:
            tur_input = input("Tür (Aksiyon, Dram vb.): ").strip()

            if tur_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not tur_input:
                print("Hata: Tür alanı boş bırakılamaz!")
                continue

            # Girilen veriyi virgüllerden ayırarak listeye dönüştürür ve boşlukları temizler.
            girilen_turler = [t.strip() for t in tur_input.split(",")]

            gecerli_secilen_turler = []
            hatali_tur_var_mi = False

            for g_tur in girilen_turler:
                eslesen_tur = None

                # Girilen türlerin sistemdeki geçerli tür listesinde olup olmadığını kontrol eder.
                for gecerli_tur in GECERLI_TURLER:
                    if gecerli_tur.lower() == g_tur.lower():
                        eslesen_tur = gecerli_tur  
                        break

                # Tür eşleştiyse ve daha önce eklenmediyse listeye dahil eder.
                if eslesen_tur:
                    if eslesen_tur not in gecerli_secilen_turler:
                        gecerli_secilen_turler.append(eslesen_tur) 
                else:
                    print(f"\nHata: '{g_tur}' adında bir film türü bulunamadı!")
                    hatali_tur_var_mi = True

            # Herhangi bir tür hatalı girildiyse tüm liste yeniden istenir
            if hatali_tur_var_mi:
                print("\nBu türlerden birini veya birkaçını seçerek tekrar yazabilirsiniz:")
                print(f"({', '.join(GECERLI_TURLER)})")
                print("-" * 40)
                continue

            # Doğrulanmış türleri aralarına virgül koyarak tek bir metin haline getirir.
            if gecerli_secilen_turler:
                tur = ", ".join(gecerli_secilen_turler)
                break

        # Otomatik artan ID mantığıyla yeni film nesnesini oluşturur ve listeye ekler.
        try:
            yeni_id = len(self.__filmler) + 1

            yeni_film = Film(yeni_id, film_adi, yonetmen, sure, tur) 
            self.__filmler.append(yeni_film) 
            print(f"\n'{film_adi}' filmi başarıyla sisteme eklendi.")
        except Exception as e: 
            print(f"Film kaydedilirken bir hata oluştu: {e}")

    # ------------------------
    # -------SALON EKLE-------
    # ------------------------
    def salon_ekle(self):
        """Kullanıcıdan terminal üzerinden salon bilgilerini alan ve sisteme kaydeden fonksiyon."""
        print("\n--- YENİ SALON EKLEME PANELİ ---")
        
        # Salon adı girişi ve boş değer/iptal kontrolü döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            salon_adi = input("Salon Adı/Numarası (Örn: Salon 1): ").strip()

            if salon_adi == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            elif salon_adi:
                break
            else:
                print("Hata: Salon adı boş bırakılamaz.")
        
        # Koltuk kapasitesi girişi ve sayısal doğrulama döngüsü.
        while True:
            kapasite_input = input("Koltuk Kapasitesi: ").strip()

            if kapasite_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not kapasite_input:
                print("Hata: kapasite boş bırakılamaz.")
                continue
                
            # Kapasite alanına geçersiz karakter veya harf girilmesi durumunda programın 
            # çökmesini engellemek için try-except bloklarıyla kontrol sağlar.
            try:
                kapasite = int(kapasite_input)

                if kapasite <= 0:
                    print("Hata: Koltuk kapasitesi 0 veya daha küçük olamaz!")
                    continue
                break
            except ValueError:
                print("Hata: Kapasite alanına sadece sayısal bir değer girmelisiniz!")

        # Doğrulanmış bilgilerle yeni salon nesnesini oluşturup sisteme dahil eder.
        yeni_salon = Salon(salon_adi, kapasite)
        self.__salonlar.append(yeni_salon)
        print(f"'{salon_adi}' başarıyla oluşturuldu.")
        
    # --------------------------
    # ------SEANS OLUŞTUR-------
    # --------------------------
    def seans_olustur(self):
        """Film ve salon seçerek yeni seans ekleyen fonksiyon."""
        print("\n--- YENİ SEANS OLUŞTURMA PANELİ ---")

        # Sistemde film veya salon tanımlı değilse işlemi baştan sonlandırır.
        if not self.__filmler or not self.__salonlar:
            print("Hata: Önce en az bir film ve salon eklemelisiniz!")
            return

        self.filmleri_listele()

        # Film seçimi ve doğrulama döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            film_input = input("Film Seçin (Sıra No): ").strip()
            
            if film_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not film_input:
                print("Hata: Film seçimi boş bırakılamaz!")
                print("-" * 40)
                continue

            try:
                # Kullanıcıdan alınan sıra numarasını liste indeksine çevirir ve geçerliliğini kontrol eder.
                film_no = int(film_input) - 1
                if 0 <= film_no < len(self.__filmler):
                    break
                else:
                    print("Hata: Geçersiz film numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")

        print("\n--- MEVCUT SALONLAR ---")
        for sira, salon in enumerate(self.__salonlar, start=1):
            print(f"{sira}-) {salon.salon_adi}")

        # Salon seçimi ve doğrulama döngüsü.
        while True:
            salon_input = input("Salon Seçin (Sıra No): ").strip()
            
            if salon_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not salon_input:
                print("Hata: Salon seçimi boş bırakılamaz!")
                continue

            try:
                # Kullanıcının seçtiği sıra numarasını liste indeksine dönüştürür.
                salon_no = int(salon_input) - 1
                if 0 <= salon_no < len(self.__salonlar):
                    break
                else:
                    print("Hata: Geçersiz salon numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")
        
        # Saat girişi ve format kontrol döngüsü.
        while True:
            saat = input("Seans Saatini Yazın (Örn: 14:30): ").strip()

            if saat == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not saat:
                print("Hata: Saat boş bırakılamaz!")
                continue
            
            try:
                # Girilen saatin SS:DD formatına uygunluğunu datetime kütüphanesiyle denetler.
                datetime.datetime.strptime(saat, "%H:%M")
                break
            except ValueError:
                print("Hata: Geçersiz saat formatı! Lütfen 24 saatlik düzende 'SS:DD' şeklinde girin (Örn: 14:30, 21:00).")

        # Koltuk sınıfı Seans sınıfından türediği için doğrudan koltuk şemasına sahip seans nesnesi üretilir.
        yeni_seans = Koltuk(self.__filmler[film_no], self.__salonlar[salon_no], saat)
        self.__seanslar.append(yeni_seans)
        print(f"\nSeans başarıyla oluşturuldu.")

    # --------------------------
    # -----FİLMLERİ LİSTELE-----
    # --------------------------
    def filmleri_listele(self):
        """Sistemde kayıtlı olan tüm filmleri sıralı bir şekilde ekrana basar."""
        print("\n--- VİZYONDAKİ FİLMLER ---")

        # Sistemde kayıtlı film yoksa kullanıcıya bilgi vererek işlemi sonlandırır.
        if not self.__filmler:
            print("Sistemde kayıtlı film bulunmamaktadır.")
            return

        # Film listesindeki her bir filmin detaylarını numaralandırarak ekrana yazdırır.
        for sira, film in enumerate(self.__filmler, start=1):
            print(f"{sira}-) Film Adı: {film.film_adi} | Yönetmen: {film.yonetmen} | Süre: {film.sure} dk | Tür: {film.tur}")

    # --------------------------
    # -----SALONLARI LİSTELE----
    # --------------------------
    def salonlari_listele(self):
        """Sistemde kayıtlı olan tüm sinema salonlarını ekrana basar."""
        print("\n--- MEVCUT SALONLAR ---")

        # Sistemde kayıtlı salon yoksa kullanıcıya bilgi vererek işlemi sonlandırır.
        if not self.__salonlar:
            print("Sistemde kayıtlı salon bulunmamaktadır.")
            return

        # Salon listesindeki her bir salonun adını ve kapasitesini numaralandırarak ekrana yazdırır.
        for sira, salon in enumerate(self.__salonlar, start=1):
            print(f"{sira}-) Salon Adı: {salon.salon_adi} | Kapasite: {salon.kapasite} Koltuk")

    # --------------------------
    # ----SEANSLARI LİSTELE-----
    # --------------------------
    def seanslari_listele(self):
        """Sisteme tanımlanmış tüm aktif seansları ekrana basar."""
        print("\n--- SEANS LİSTESİ ---\n")

        # Sistemde kayıtlı seans yoksa kullanıcıya bilgi vererek işlemi sonlandırır.
        if not self.__seanslar:
            print("Henüz seans eklenmedi.")
            return

        # Mevcut seansların film, salon ve saat bilgilerini numaralandırarak ekrana yazdırır.
        for sira, seans in enumerate(self.__seanslar, start=1):
            print(f"{sira}-) Film: {seans.film.film_adi} | Salon: {seans.salon.salon_adi} | Saat: {seans.saat}")

    # --------------------------
    # -------KAYIT SİLME--------
    # --------------------------
    def kayit_silme(self):
        """Sistemde kayıtlı olan film, salon veya seans verilerini kalıcı olarak siler."""
        print("\n--- KAYIT SİLME PANELİ ---\n")

        print("1- Film Kaydını Sil")
        print("2- Salon Kaydını Sil")
        print("3- Seans Programını İptal Et\n")

        # Kullanıcıdan geçerli bir menü tercihi alınana kadar girdi kontrolü sağlar.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            secim = input("Lütfen silmek istediğiniz veri türünü seçiniz (1-3): ").strip()
            
            if secim == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            elif not secim:
                print("Hata: Seçim alanı boş bırakılamaz!\n")
                continue
            elif secim in ["1", "2", "3"]:
                break
            else:
                print("Hata: Geçersiz seçim! Lütfen sadece '1', '2', '3' veya 'q' giriniz.\n")

        if secim == "1":
            # Sistemde kayıtlı film yoksa işlemi baştan sonlandırır.
            if not self.__filmler:
                print("\nHata: Sistemde silinebilecek kayıtlı bir film bulunamadı!")
                return

            self.filmleri_listele()

            # Film seçimi ve doğrulama döngüsü.
            while True:
                film_input = input("Film Seçin (Sıra No): ").strip()

                if film_input == 'q':
                    print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                    return
                if not film_input:
                    print("Hata: Film seçimi boş bırakılamaz!")
                    continue
                try:
                    # Girilen değerin sayısal bütünlüğünü ve film listesinin sınırları içinde olup olmadığını doğrular.
                    film_no = int(film_input) - 1
                    if 0 <= film_no < len(self.__filmler):
                        break
                    else:
                        print("Hata: Geçersiz film numarası! Listeden bir sıra numarası seçin.")
                except ValueError:
                    print("Hata: Lütfen geçerli bir sayı girin!")

            # Seçilen film nesnesini listeden çıkarır.
            silinen_film = self.__filmler.pop(film_no)

            # Silinen filme ait tüm seansları sistemden temizler.
            self.__seanslar = [s for s in self.__seanslar if s.film.film_id != silinen_film.film_id]
            print(f"\n'{silinen_film.film_adi}' filmi ve filme ait tüm seanslar sistemden başarıyla kaldırıldı.")

        elif secim == "2":
            # Sistemde kayıtlı salon yoksa işlemi baştan sonlandırır.
            if not self.__salonlar:
                print("\nHata: Sistemde silinebilecek kayıtlı bir salon bulunamadı!")
                return
            
            self.salonlari_listele()

            # Salon seçimi ve doğrulama döngüsü.
            while True:
                salon_input = input("Salon Seçin (Sıra No): ").strip()

                if  salon_input == 'q':
                    print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                    return
                if not salon_input:
                    print("Hata: Salon seçimi boş bırakılamaz!")
                    continue
                try:
                    # Girilen değerin sayısal bütünlüğünü ve salon listesinin sınırları içinde olup olmadığını doğrular.
                    salon_no = int(salon_input) - 1
                    if 0 <= salon_no < len(self.__salonlar):
                        break
                    else:
                        print("Hata: Geçersiz salon numarası! Listeden bir sıra numarası seçin.")
                except ValueError:
                    print("Hata: Lütfen geçerli bir sayı girin!")

            # Seçilen salon nesnesini listeden çıkarır.
            silinen_salon = self.__salonlar.pop(salon_no)

            # Silinen salona ait tüm seansları sistemden temizler.
            self.__seanslar = [s for s in self.__seanslar if s.salon.salon_adi != silinen_salon.salon_adi]
            print(f"\n'{silinen_salon.salon_adi}' salonu ve salona ait tüm seanslar sistemden başarıyla kaldırıldı.")

        elif secim == "3":
            # Sistemde kayıtlı seans yoksa işlemi baştan sonlandırır.
            if not self.__seanslar:
                print("\nHata: Sistemde silinebilecek kayıtlı bir seans bulunamadı!")
                return
            self.seanslari_listele()

            # Seans seçimi ve doğrulama döngüsü.
            while True:
                seans_input = input("\nSeans Seçin (Sıra No): ").strip()

                if  seans_input == 'q':
                    print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                    return
                if not seans_input:
                    print("Hata: Seans seçimi boş bırakılamaz!")
                    continue
                try:
                    # Girilen değerin sayısal bütünlüğünü ve seans listesinin sınırları içinde olup olmadığını doğrular.
                    seans_no = int(seans_input) - 1
                    if 0 <= seans_no < len(self.__seanslar):
                        break
                    else:
                        print("Hata: Geçersiz seans numarası! Listeden bir sıra numarası seçin.")
                except ValueError:
                    print("Hata: Lütfen geçerli bir sayı girin!")

            # Seçilen seans nesnesini listeden çıkararak programı iptal eder.
            silinen_seans = self.__seanslar.pop(seans_no)
            print(f"\n{silinen_seans.film.film_adi} Filminin '{silinen_seans.saat}' seansı sistemden başarıyla kaldırıldı.")

    # --------------------------
    # ------KOLTUK DURUMU-------
    # --------------------------
    def koltuk_durumu_goruntule(self):
        """Seçilen seansın koltuk planını ekrana basar."""

        # Gösterilebilecek hiçbir seans yoksa baştan uyarı vererek işlemi sonlandırır.
        if not self.__seanslar:
            print("Henüz seans eklenmedi.")
            return

        self.seanslari_listele()

        # Seans seçimi ve doğrulama döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            seans_input = input("\nSeans numarası seçin: ").strip()
            
            if seans_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not seans_input:
                print("Hata: Seans seçimi boş bırakılamaz!")
                continue

            try:
                # Kullanıcının seçtiği sıra numarasını liste indeksine dönüştürür.
                seans_no = int(seans_input) - 1
                if 0 <= seans_no < len(self.__seanslar):
                    self.__seanslar[seans_no].koltuk_durumu_goster()
                    break
                else:
                    print("Hata: Geçersiz seans numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")

    # --------------------------
    # --------BİLET SAT---------
    # --------------------------
    def bilet_sat(self):
        """Film, seans ve koltuk seçimi adımlarıyla bilet satışı gerçekleştirir."""
        print("\n--- BİLET SATIŞ PANELİ ---")

        # Sistemde kayıtlı film yoksa bilet satış işlemini baştan sonlandırır.
        if not self.__filmler:
            print("Hata: sistemde kayıtlı film bulunmamaktadır!")
            return
            
        self.filmleri_listele()
        # Film seçimi ve doğrulama döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            film_input = input("Film Seçin (Sıra No): ").strip()

            if film_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not film_input:
                print("Hata: Film seçimi boş bırakılamaz!")
                continue
            try:
                film_no = int(film_input) - 1
                if 0 <= film_no < len(self.__filmler):
                    break
                else:
                    print("Hata: Geçersiz film numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")
        
        secilen_film = self.__filmler[film_no]

        # Seçilen filme ait seansları filtreleyerek ayrı bir listeye aktarır.
        filme_ait_seanslar = [seans for seans in self.__seanslar if seans.film.film_id == secilen_film.film_id]

        # Seçilen filme ait aktif bir seans planı yoksa işlemi sonlandırır.
        if not filme_ait_seanslar:
            print(f"\nHata: '{secilen_film.film_adi}' filmi için tanımlanmış bir seans bulunamadı!")
            return
        
        print(f"\n--- {secilen_film.film_adi} Filminin Seansları ---")
        for sira, seans in enumerate(filme_ait_seanslar, 1):
            print(f"{sira}. Salon: {seans.salon.salon_adi} | Saat: {seans.saat}")

        # Seans seçimi ve doğrulama döngüsü.
        while True:
            seans_input = input("\nSeans Seçin (Sıra No): ").strip()

            if seans_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not seans_input:
                print("Hata: Seans seçimi boş bırakılamaz!")
                continue

            try:
                seans_no = int(seans_input) - 1
                if 0 <= seans_no < len(filme_ait_seanslar):
                    break
                else:
                    print("Hata: Geçersiz seans numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")
        
        secilen_seans = filme_ait_seanslar[seans_no]
        print(f"\nSeçilen Seans onaylandı: {secilen_seans.salon.salon_adi} - {secilen_seans.saat}")

        # Koltuk haritasını kullanıcının görebilmesi için ekrana basar.
        secilen_seans.koltuk_durumu_goster()

        # Geçerli ve boş bir koltuk seçilene kadar çalışan doğrulama döngüsü.
        while True:
            try:
                sira = input("Koltuk Sırası (örn: 'A-H'): ").strip().upper()
                numara = int(input("Koltuk Numarası (örn: '1-10'): "))

                # Girilen koltuğun salon şemasına ve sınır değerlere uygunluğunu kontrol eder.
                if sira in secilen_seans.koltuklar and 1 <= numara <= 10:
                    # Koltuk değeri False ise boştur ve satın alınmaya uygundur.
                    if not secilen_seans.koltuklar[sira][numara]:

                        # Bilet türü seçimi ve ücretlendirme döngüsü.
                        while True:
                            print("\nBilet Türünü Seçiniz:")
                            print("1- Tam Bilet (250 TL)")
                            print("2- Öğrenci Bileti (200 TL)")
                            tur_secimi = input("Seçiminiz (1 veya 2): ").strip()

                            if tur_secimi == 'q':
                                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                                return
                            
                            elif tur_secimi == "1":
                                bilet_fiyati = 250
                                bilet_tipi = "Tam Bilet"
                                break

                            elif tur_secimi == "2":
                                bilet_fiyati = 200
                                bilet_tipi = "Öğrenci Bileti"
                                break

                            else:
                                print("Hata: Geçersiz seçim! Lütfen sadece '1' veya '2' yazınız.")

                        yeni_bilet = Bilet(bilet_tipi, bilet_fiyati, sira, numara)

                        yeni_bilet.satis_tarihi = datetime.date.today()

                        # Koltuk koordinatına bilet nesnesini atayarak koltuğu doldurur ve geliri günceller.
                        secilen_seans.koltuklar[sira][numara] = yeni_bilet
                        self.__toplam_gelir += bilet_fiyati

                        print(f"\nBilet satıldı: {sira}{numara} koltuğu için {bilet_tipi} satıldı.")
                        print(f"\nÖdenen Tutar: {bilet_fiyati} TL")
                        break
                    else:
                        print(f"\nHata: {sira}{numara} koltuğu zaten dolu!")
                else:
                    print("\nHata: Geçersiz koltuk seçimi!")
            except ValueError:
                print("Hata: Lütfen geçerli bir koltuk seçin!")

    # --------------------------
    # -----BİLET İPTAL ET-------
    # --------------------------
    def bilet_iptal(self):
        """Satılan bir koltuğun rezervasyonunu iptal ederek koltuğu tekrar boş (False) durumuna getirir."""
        print("\n--- BİLET İPTAL PANELİ ---")

        # Sistemde kayıtlı film yoksa iptal edilebilecek bir bilet de olamayacağı için işlemi sonlandırır.
        if not self.__filmler:
            print("Hata: Sistemde kayıtlı film bulunamadı!")
            return

        self.filmleri_listele()

        # İptal edilecek filmin seçimi ve doğrulama döngüsü.
        while True:
            print("[Menüye Dönmek İçin 'q']")
            film_input = input("İptal Edilecek Filmi Seçin (Sıra No): ").strip()

            if film_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not film_input:
                print("Hata: Film seçimi boş bırakılamaz!")
                continue
            try:
                film_no = int(film_input) - 1
                if 0 <= film_no < len(self.__filmler):
                    break
                else:
                    print("Hata: Geçersiz film numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")

        secilen_film = self.__filmler[film_no]

        # İptal işlemine ait seansları filtreleyerek ayrı bir listeye aktarır.
        filme_ait_seanslar = [seans for seans in self.__seanslar if seans.film.film_id == secilen_film.film_id]

        if not filme_ait_seanslar:
            print(f"\nHata: '{secilen_film.film_adi}' filmi için tanımlanmış bir seans bulunamadı!")
            return

        print(f"\n--- {secilen_film.film_adi} Filminin Seansları ---")
        for sira, seans in enumerate(filme_ait_seanslar, 1):
            print(f"{sira}. Salon: {seans.salon.salon_adi} | Saat: {seans.saat}")

        # Seans seçimi ve doğrulama döngüsü.
        while True:
            seans_input = input("\nSeans Seçin (Sıra No): ").strip()

            if seans_input == 'q':
                print("\nİşlem iptal edildi. Ana menüye dönülüyor...")
                return
            if not seans_input:
                print("Hata: Seans seçimi boş bırakılamaz!")
                continue
            try:
                seans_no = int(seans_input) - 1
                if 0 <= seans_no < len(filme_ait_seanslar):
                    break
                else:
                    print("Hata: Geçersiz seans numarası! Listeden bir sıra numarası seçin.")
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin!")

        secilen_seans = filme_ait_seanslar[seans_no]

        # Güncel koltuk durum haritasını ekrana basar.
        secilen_seans.koltuk_durumu_goster()

        satilmis_bilet_var_mi = False

        # Seçilen seansta en az bir koltuğun dolu olup olmadığını kontrol eder.
        for s in secilen_seans.koltuklar:
            for n in secilen_seans.koltuklar[s]:
                if secilen_seans.koltuklar[s][n] != False:
                    satilmis_bilet_var_mi = True
                    break

        # Seansta satılmış tek bir bilet bile yoksa işlemi baştan sonlandırır.                
        if not satilmis_bilet_var_mi:
            print(f"\nHata: Seçilen seansta ({secilen_seans.salon.salon_adi} - {secilen_seans.saat}) henüz hiç bilet satılmamıştır!")
            return
        
        # Geçerli ve iptal edilebilir bir koltuk seçilene kadar çalışan doğrulama döngüsü.
        while True:
            try:
                sira = input("İptal Edilecek Koltuk Sırası (A-H): ").strip().upper()
                numara = int(input("İptal Edilecek Koltuk Numarası (1-10): "))

                if sira in secilen_seans.koltuklar and 1 <= numara <= 10:                   
                    # Koltuk değeri False değilse içinde bilet nesnesi barındırır ve iptale uygundur.
                    if secilen_seans.koltuklar[sira][numara] != False:
                        mevcut_bilet = secilen_seans.koltuklar[sira][numara]
                        iade_tutari = mevcut_bilet.fiyat

                        # Toplam gelirden iade tutarını düşer ve koltuk verisini False (boş) olarak günceller.
                        self.__toplam_gelir -= iade_tutari
                        secilen_seans.koltuklar[sira][numara] = False

                        print(f"\nBaşarılı: {sira}{numara} koltuğunun bileti iptal edildi ve koltuk boşa çıktı.")
                        print(f"{iade_tutari} TL iade edildi.")
                        break 
                    else:
                        print(f"\nHata: {sira}{numara} koltuğu zaten boş! İptal edilecek bir bilet yok.")
                else:
                    print("\nHata: Geçersiz koltuk seçimi! Sıra A-H, numara 1-10 arasında olmalıdır.")

            except ValueError:
                print("Hata: Lütfen geçerli bir koltuk seçin!")

    # --------------------------
    # ------SATIŞ RAPORU--------
    # --------------------------
    def rapor_goster(self):
        """Günlük toplam doluluk oranını ve kasadaki net kazancı ekrana basar."""

        bugun_tarih = datetime.date.today()

        # Güncel tarihe ait bilet olup olmadığını denetleyen kontrol bayrağı.
        bugun_bilet_var_mi = False

        print("\n=========================================")
        print(f"     GÜNLÜK SATIŞ RAPORU ({bugun_tarih})")
        print("=========================================")
        
        ogrenci_sayisi = 0
        tam_sayisi = 0
        
        # Tüm seansları ve koltukları tarayarak bilet kategorilerini ve sayılarını hesaplar.
        for seans in self.__seanslar:
            for sira in seans.koltuklar:
                for numara in seans.koltuklar[sira]:
                    if seans.koltuklar[sira][numara] != False:
                        bilet_objesi = seans.koltuklar[sira][numara]

                        # Biletin satış tarihinin bugünün tarihiyle eşleşip eşleşmediğini kontrol eder.
                        if hasattr(bilet_objesi, 'satis_tarihi') and bilet_objesi.satis_tarihi == bugun_tarih:
                            bugun_bilet_var_mi = True

                            # Bilet türüne göre ilgili sayaç değerlerini artırır.
                            if bilet_objesi.bilet_tipi == "Öğrenci Bileti":
                                ogrenci_sayisi += 1
                            else:
                                tam_sayisi += 1
                        else:
                            # Tarihi geçmiş olan eski biletlerin koltuk rezervasyonlarını temizleyerek boşa çıkarır.
                            seans.koltuklar[sira][numara] = False

        # Gün değiştiğinde ve bugüne ait bilet bulunamadığında toplam hasılat bilgisini sıfırlar.
        if not bugun_bilet_var_mi:
            self.__toplam_gelir = 0
        
        toplam_satilan_bilet = ogrenci_sayisi + tam_sayisi

        if toplam_satilan_bilet == 0:
            print("(Henüz satılmış bir bilet bulunmuyor.)")
        
        print(f"Satılan Öğrenci Bileti     : {ogrenci_sayisi}")
        print(f"Satılan Tam Bilet          : {tam_sayisi}")
        print(f"Toplam Satılan Bilet Adedi : {toplam_satilan_bilet}")
        print("-" * 40)
        print(f"Kasadaki Toplam Hasılat    : {self.__toplam_gelir} TL")
        print("=========================================")

    # --------------------------
    # -----VERİLERİ KAYDET------
    # --------------------------
    def verileri_kaydet(self):
        """Sistemdeki nesne listelerini ve finansal verileri pkl dosyasına kaydeder."""
        try:
            # Sistemdeki tüm nesne listelerini ve mali verileri tek bir sözlük yapısında birleştirir.
            veriler = {
                "filmler": self.__filmler,
                "salonlar": self.__salonlar,
                "seanslar": self.__seanslar,
                "toplam_gelir": self.__toplam_gelir
            }
            # Belirtilen dosyayı ikili yazma (wb) modunda açarak verileri pkl formatında diske kaydeder.
            with open("data.pkl", "wb") as dosya:
                pickle.dump(veriler, dosya) 
                
            print("\nBaşarılı: Tüm veriler PKL formatında sisteme güvenle kaydedildi!")
        except Exception as e:
            print(f"Veriler kaydedilirken bir hata oluştu: {e}")

    # --------------------------
    # ------VERİLERİ YÜKLE------
    # --------------------------
    def verileri_yukle(self):
        """Kayıtlı olan tüm nesne ve verileri pkl dosyasından geri okuyarak sisteme yükler."""
        try:
            # Dosyayı ikili okuma modunda ('rb') açarak kaydedilmiş pkl verilerini belleğe alır.
            with open("data.pkl", "rb") as dosya:
                veriler = pickle.load(dosya)
            
            # Sözlükten okunan listeleri sistemdeki ilgili gizli özniteliklere geri yükler
            self.__filmler = veriler["filmler"]
            self.__salonlar = veriler["salonlar"]
            self.__seanslar = veriler["seanslar"]
            self.__toplam_gelir = veriler.get("toplam_gelir", 0)

            # Salonlardaki tüm koltukları tarayarak bugünün tarihine ait bilet olup olmadığını sorgular.
            bugun_bilet_var_mi = any(
                bilet.satis_tarihi == datetime.date.today()
                for seans in self.__seanslar
                for sira in seans.koltuklar
                for numara in seans.koltuklar[sira]
                if (bilet := seans.koltuklar[sira][numara]) != False and hasattr(bilet, 'satis_tarihi')
            )
            # Bugüne ait satılmış herhangi bir bilet bulunamadığı takdirde kasadaki geliri sıfırlar.
            if not bugun_bilet_var_mi:
                self.__toplam_gelir = 0
            
            print("\nBaşarılı: Eski veriler bilgisi başarıyla yüklendi!")
        except FileNotFoundError:
            print("\nHata: Kayıtlı bir veri dosyası ('data.pkl') bulunamadı!")
        except Exception as e:
            print(f"Veriler yüklenirken bir hata oluştu: {e}")

# =========================================
# =====MENÜ VE PROGRAM AKIŞI ALTYAPISI=====
# =========================================
def ana_menu():
    sistem = SinemaSistemi()

    # Kullanıcı çıkış yapana kadar ana menü arayüzünü ekranda tutan döngü.
    while True:
        print("\n===================================")
        print("===SİNEMA BİLET VE SALON SİSTEMİ===")
        print("===================================")
        print("1- Film ekle")
        print("2- Salon ekle")
        print("3- Seans oluştur")
        print("4- Filmleri listele")
        print("5- Salonları listele")
        print("6- Seansları listele")
        print("7- Kayıt sil")
        print("8- Koltuk durumunu görüntüle")
        print("9- Bilet sat")
        print("10- Bilet iptal et")
        print("11- Günlük bilet satış raporu")
        print("12- Verileri kaydet")
        print("13- Verileri yükle")
        print("0- Çıkış")
        print("===================================")

        secim = input("Lütfen yapmak istediğiniz işlemi seçin: ").strip()

        # Kullanıcının seçimine göre ilgili yönetim fonksiyonunu tetikler.
        if secim == "1":
            sistem.film_ekle()
        elif secim == "2":
            sistem.salon_ekle()
        elif secim == "3":
            sistem.seans_olustur()
        elif secim == "4":
            sistem.filmleri_listele()
        elif secim == "5":
            sistem.salonlari_listele()
        elif secim == "6":
            sistem.seanslari_listele()
        elif secim == "7":
            sistem.kayit_silme()
        elif secim == "8":
            sistem.koltuk_durumu_goruntule()
        elif secim == "9":
            sistem.bilet_sat()
        elif secim == "10":
            sistem.bilet_iptal()
        elif secim == "11":
            sistem.rapor_goster()
        elif secim == "12":
            sistem.verileri_kaydet()
        elif secim == "13":
            sistem.verileri_yukle()
        elif secim == "0":
            print("Programdan çıkılıyor. İyi günler!")
            break
        else:
            print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin!")

# Kod doğrudan ana dosya üzerinden çalıştırıldığında menü döngüsünü başlatır.
if __name__ == "__main__":
    ana_menu()
