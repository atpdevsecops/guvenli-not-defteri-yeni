# Güvenli Not Defteri Projesi

**DevSecOps Pratikleri için Python Flask Tabanlı Not Defteri Uygulaması**

Bu proje, temel bir not defteri uygulaması üzerinden güvenli yazılım geliştirme (DevSecOps) prensiplerinin ve pratiklerinin nasıl uygulanabileceğini göstermek amacıyla geliştirilmiştir. Hem geliştiricilere güvenli kodlama konusunda farkındalık kazandırmayı hem de temel DevSecOps araç ve süreçlerinin entegrasyonuna dair bir örnek sunmayı hedefler.

## 🚀 Proje Hakkında

Güvenli Not Defteri, kullanıcıların basit metin tabanlı notlar oluşturmasına, görüntülemesine, güncellemesine ve silmesine olanak tanıyan bir web uygulamasıdır. Uygulamanın geliştirme yaşam döngüsüne çeşitli güvenlik kontrolleri ve pratikleri entegre edilmiştir.

## ✨ Özellikler (Potansiyel ve Hedeflenen)

* **Not Yönetimi:**
    * Yeni not oluşturma
    * Mevcut notları listeleme
    * Not detaylarını görüntüleme
    * Notları düzenleme
    * Notları silme
* **Güvenlik Özellikleri (Örnek Amaçlı):**
    * Temel kullanıcı kimlik doğrulama (Geliştirilebilir)
    * Giriş doğrulama (Input Validation) mekanizmaları
    * Güvenli HTTP başlıkları (Security Headers)
    * Hata yönetimi ve loglama
    * Veritabanı etkileşimlerinde parametrik sorgular (SQL Injection önlemi olarak)
* **DevSecOps Entegrasyonları (Gösterim Amaçlı):**
    * Bağımlılık zafiyeti taraması (`requirements.txt` üzerinden)
    * Dockerfile ile güvenli imaj oluşturma pratikleri
    * (Gelecekte eklenebilir) Statik Kod Analizi (SAST) ve Dinamik Kod Analizi (DAST) araçlarıyla entegrasyon için yapılandırma örnekleri.

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.x, Flask
* **Veritabanı:** (Projenin basitliğine göre SQLite veya dosya tabanlı bir sistem olabilir. Gerçek bir senaryoda daha güvenli bir DB seçimi önemlidir.)
* **Konteynerizasyon:** Docker
* **Diğer Araçlar:** (Projenin gelişimine göre eklenebilir, örn: Snyk, Bandit, OWASP ZAP)

## ⚙️ Kurulum ve Başlatma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

### Gereksinimler

* Python 3.8+
* pip (Python paket yöneticisi)
* Git
* Docker (Eğer konteyner olarak çalıştırmak isterseniz)

### Adım Adım Kurulum

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/atpdevsecops/guvenli-not-defteri.git](https://github.com/atpdevsecops/guvenli-not-defteri.git)
    cd guvenli-not-defteri
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin (Önerilir):**
    ```bash
    python -m venv venv
    # Windows için:
    # venv\Scripts\activate
    # macOS/Linux için:
    # source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı Başlatın:**
    ```bash
    python app.py
    ```
    Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışmaya başlayacaktır.

### 🐳 Docker ile Çalıştırma

1.  **Docker Image'ını Oluşturun:**
    ```bash
    docker build -t guvenli-not-defteri .
    ```

2.  **Docker Konteynerini Başlatın:**
    ```bash
    docker run -p 5000:5000 guvenli-not-defteri
    ```
    Uygulama `http://localhost:5000` adresinde erişilebilir olacaktır.

## 🛡️ DevSecOps Pratikleri ve Gösterimleri

Bu proje aşağıdaki DevSecOps pratiklerini göstermeyi veya entegrasyonuna zemin hazırlamayı amaçlar:

* **Güvenli Kodlama Standartları:**
    * **Giriş Doğrulama (Input Validation):** Kullanıcıdan alınan verilerin (örneğin not içeriği) beklenen formatta ve zararsız olduğundan emin olmak.
    * **Hata Yönetimi:** Detaylı hata mesajlarının son kullanıcıya sızdırılmaması, ancak loglarda yeterli bilginin bulunması.
    * **Parametrik Sorgular:** Eğer bir SQL veritabanı kullanılıyorsa, SQL Injection saldırılarını önlemek için.
* **Bağımlılık Yönetimi ve Taraması:**
    * `requirements.txt` ile kullanılan kütüphanelerin versiyonlarının sabitlenmesi.
    * Bu kütüphanelerdeki bilinen zafiyetlerin taranması için `Snyk`, `Safety` gibi araçların kullanılabileceğinin gösterilmesi.
* **Konteyner Güvenliği:**
    * `Dockerfile` içerisinde en az yetki prensibine uygun kullanıcı tanımlanması.
    * Gereksiz paketlerin imaja dahil edilmemesi.
    * Konteyner imajlarının zafiyet taramasından geçirilmesi (örneğin `Trivy` veya Docker Hub'ın kendi tarama özellikleri).
* **Statik Kod Analizi (SAST):**
    * `Bandit`, `SonarLint` gibi araçlarla kod tabanındaki potansiyel güvenlik açıklarının erken aşamada tespit edilmesi. (Bu projeye entegre edilebilir bir sonraki adım olarak düşünülebilir.)
* **Dinamik Kod Analizi (DAST):**
    * Çalışan uygulama üzerinde `OWASP ZAP` gibi araçlarla otomatize güvenlik testleri yapılması. (Bu projeye entegre edilebilir bir sonraki adım olarak düşünülebilir.)
* **Gizli Bilgi Yönetimi (Secrets Management):**
    * API anahtarları, veritabanı şifreleri gibi hassas bilgilerin kod içinde açıkça yazılmaması, ortam değişkenleri veya özel araçlarla yönetilmesi.

## 📂 Proje Yapısı (Örnek)

```
guvenli-not-defteri/
├── app.py                # Ana Flask uygulaması
├── requirements.txt      # Python bağımlılıkları
├── Dockerfile            # Docker imajı oluşturma talimatları
├── .dockerignore         # Docker build'de hariç tutulacak dosyalar
├── .gitignore            # Git tarafından izlenmeyecek dosyalar
├── static/               # (Varsa) CSS, JS, resim dosyaları
│   └── style.css
├── templates/            # (Varsa) HTML şablonları
│   ├── index.html
│   └── note.html
├── README.md             # Bu dosya
└── LICENSE               # Proje lisansı
```

## 🤝 Katkıda Bulunma

Katkılarınız projeyi daha da geliştirmemize yardımcı olacaktır! Lütfen bir "issue" açarak veya "pull request" göndererek katkıda bulunun.

1.  Projeyi Fork'layın.
2.  Kendi branch'inizi oluşturun (`git checkout -b ozellik/yeni-ozellik`).
3.  Değişikliklerinizi commit'leyin (`git commit -am 'Yeni bir özellik eklendi'`).
4.  Branch'inizi push'layın (`git push origin ozellik/yeni-ozellik`).
5.  Bir Pull Request oluşturun.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.
