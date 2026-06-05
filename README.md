# Sinema Bilet ve Salon Yönetim Sistemi

## Proje Amacı
Bu projenin amacı, bir sinema işletmesinin temel işleyiş mekanizmalarını (film veri tabanı, salon kapasiteleri, seans planlamaları, dinamik koltuk matrisleri ve biletleme süreçleri) merkezi bir sistem üzerinden simüle etmektir. Proje; ilişkisel veri yapılarını korumayı, satılan koltuğun tekrar satılmasını engellemeyi, finansal raporlamayı ve verilerin oturumlar arası kalıcılığını nesne yönelimli programlama prensipleriyle çözmeyi hedeflemektedir.

## Kullanılan Teknolojiler
- **Python** (Programlama Dili)
- **PKL (Pickle)** (Nesne Serileştirme ve Veri Saklama)
- **OOP** (Nesne Yönelimli Programlama)

## Kullanılan OOP Yapıları
- **Class (Sınıf):** `Film`, `Salon`, `Seans`, `Koltuk`, `Bilet` ve `SinemaSistemi` adlarında işlevsel sınıflar tanımlanmıştır.
- **Object (Nesne):** Her yeni film, salon, seans veya satılan bilet sistem içinde birer nesne olarak üretilir ve listelerde saklanır.
- **Inheritance (Kalıtım):** `Koltuk` sınıfı, `Seans` sınıfından miras (`Seans.__init__(self, film, salon, saat)`) alarak seans özelliklerini genişletmiştir.
- **Encapsulation (Kapsülleme):** Kritik veriler (`__filmler`, `__koltuklar`, `__toplam_gelir` vb.) çift alt çizgi ile gizlenmiş ve dışarıdan manipülasyonu engellemek için `@property` dekoratörü ile salt okunur (read-only) erişim sağlanmıştır.
- **Polymorphism (Çok Biçimlilik):** `Koltuk` sınıfının, miras aldığı temel `Seans` sınıfının yapısını korurken üzerine yeni koltuk hazırlama ve matris listeleme davranışları eklemesiyle uygulanmıştır.
- **Abstraction (Soyutlama):** Kullanıcının karmaşık koltuk şeması hesaplamalarını veya dosya okuma/yazma süreçlerini görmeden, menü üzerinden sadece basit fonksiyonları tetikleyerek işlem yapabilmesi sağlanmıştır.

## Proje Özellikleri
- **Kullanıcı/Kayıt Ekleme:** Terminal paneli üzerinden doğrulamalı film, salon ve seans planı ekleme desteği.
- **Listeleme:** Vizyondaki filmleri, salonları, aktif seansları ve anlık koltuk doluluk şemasını (`O`/`X` matrisi) listeleme özelliği.
- **Arama / Kontrol:** Girilen film türlerinin geçerliliğini denetleyen arama algoritması ve seans bilet tarihlerinin kontrolü.
- **Kayıt Silme (Ek Özellik):** Eklenen film, salon veya seans verilerini sistemden ve bağlı olduğu diğer yapılardan kalıcı olarak temizleme imkanı.
- **Dosyaya Kayıt:** Sistemdeki tüm canlı nesneleri ve finansal kasayı tek tuşla `data.pkl` dosyasına ikili (binary) formatta kaydetme.
- **Dosyadan Veri Yükleme:** Kayıtlı dosyayı okuyarak geçmiş oturumu, koltuk durumlarını ve ciro raporunu sisteme kayıpsız geri yükleme.

## Menu
```
===================================
===SİNEMA BİLET VE SALON SİSTEMİ===
===================================
1- Film ekle
2- Salon ekle
3- Seans oluştur
4- Filmleri listele
5- Salonları listele
6- Seansları listele
7- Kayıt sil
8- Koltuk durumunu görüntüle
9- Bilet sat
10- Bilet iptal et
11- Günlük bilet satış raporu
12- Verileri kaydet
13- Verileri yükle
0- Çıkış
===================================
```

## Kurulum
Projeyi çalıştırmak için terminal veya komut satırından proje dizinine giderek şu komutu yazmanız yeterlidir:

```bash
python main.py
```

## Geliştirenler
**Ders:** [Programlama 2]

- **Ad Soyad:** [Mert ADA] | **Öğrenci No:** [2519181041]
- **Ad Soyad:** [Necati Fehmi Bal] | **Öğrenci No:** [2519181015]
- **Ad Soyad:** [Furkan Ada Seval] | **Öğrenci No:** [2519181027]
