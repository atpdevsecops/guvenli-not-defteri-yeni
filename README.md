# Güvenli Not Defteri Projesi

**DevSecOps Pratikleri için Python Flask Tabanlı Not Defteri Uygulaması**

Güvenli Not Defteri, modern web uygulamalarında güvenli yazılım geliştirme (DevSecOps) prensiplerini ve pratiklerini somut bir şekilde sergilemek üzere tasarlanmış, Python Flask tabanlı bir not defteri uygulamasıdır. Bu proje, geliştiricilere güvenli kodlama alışkanlıkları kazandırmak ve temel DevSecOps araç/süreç entegrasyonlarını canlı bir örnek üzerinde göstermek için geliştirilmiştir.

## 🚀 Proje Hakkında

Güvenli Not Defteri, kullanıcıların metin tabanlı notlarını güvenli bir şekilde oluşturmasına, görüntülemesine, güncellemesine ve silmesine imkan tanır. Uygulamanın tüm geliştirme yaşam döngüsü boyunca çeşitli güvenlik kontrolleri ve en iyi pratikler göz önünde bulundurulmuştur.

## ✨ Özellikler

* **Not Yönetimi:**
    * Yeni not oluşturma
    * Mevcut notları listeleme
    * Not detaylarını görüntüleme
    * Notları düzenleme
    * Notları silme
* **Güvenlik Özellikleri:**
    * Kullanıcı kimlik doğrulama ve yetkilendirme mekanizmaları
    * Gelişmiş giriş doğrulama (Input Validation) ve çıktı kodlama (Output Encoding) teknikleri
    * Önerilen güvenli HTTP başlıkları (Security Headers) uygulaması
    * Güvenli hata yönetimi ve detaylı loglama (hassas bilgi sızıntısını önleyerek)
    * Veritabanı etkileşimlerinde SQL Injection ve benzeri zafiyetlere karşı koruma (örn: ORM veya parametrik sorgular)
* **DevSecOps Entegrasyonları:**
    * `requirements.txt` ile bağımlılık yönetimi ve bilinen zafiyetler için otomatik tarama entegrasyonu (örneğin `pip-audit`, `Snyk` ile)
    * `Dockerfile` ile güvenli ve optimize edilmiş konteyner imajı oluşturma pratikleri
    * Statik Kod Analizi (SAST) araçları (örn: `Bandit`) ile kod üzerinden güvenlik taraması entegrasyonu
    * Dinamik Kod Analizi (DAST) araçları (örn: `OWASP ZAP`) ile çalışan uygulama üzerinde güvenlik testi yetenekleri

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.x, Flask
* **Veritabanı:** Proje, kolay kurulum ve taşınabilirlik için SQLite kullanmaktadır. Farklı veritabanı sistemleriyle entegrasyon için yapılandırılabilir.
* **Konteynerizasyon:** Docker
* **Güvenlik Araçları (Entegre/Önerilen):** `Bandit`, `pip-audit` (veya `Safety`/`Snyk`), `OWASP ZAP`

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

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
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

Bu proje, aşağıdaki DevSecOps pratiklerini aktif olarak uygular ve sergiler:

* **Güvenli Kodlama Standartları:**
    * **Giriş Doğrulama (Input Validation):** Kullanıcıdan alınan tüm veriler, güvenlik risklerini en aza indirmek için titizlikle doğrulanır ve temizlenir.
    * **Hata Yönetimi:** Uygulama, son kullanıcıya gereksiz teknik detaylar sızdırmadan, geliştiriciler için anlamlı loglar üreten güvenli bir hata yönetimi stratejisi izler.
    * **Güvenli Veritabanı Erişimi:** Veritabanı işlemleri, SQL enjeksiyonu gibi yaygın zafiyetleri engellemek için güvenli yöntemlerle (örn: Object-Relational Mapper veya parametreli sorgular) gerçekleştirilir.
* **Bağımlılık Yönetimi ve Taraması:**
    * Proje bağımlılıkları `requirements.txt` dosyasında net bir şekilde tanımlanmış olup, bilinen zafiyetlere karşı düzenli olarak taranması için `pip-audit` gibi araçlar entegre edilmiştir.
* **Konteyner Güvenliği:**
    * `Dockerfile`, en az yetki prensibi (Principle of Least Privilege) doğrultusunda yapılandırılmıştır.
    * İmaj boyutunu optimize etmek ve saldırı yüzeyini azaltmak için çok aşamalı derlemeler (multi-stage builds) ve gereksiz bağımlılıkların kaldırılması gibi teknikler kullanılır.
    * Oluşturulan imajlar, bilinen zafiyetlere karşı taranır (örn: `Trivy`).
* **Otomatik Güvenlik Testleri:**
    * **Statik Kod Analizi (SAST):** `Bandit` gibi araçlar, geliştirme sürecinin erken aşamalarında potansiyel güvenlik açıklarını belirlemek için kod tabanını otomatik olarak analiz eder.
    * **Dinamik Kod Analizi (DAST):** Çalışan uygulama üzerinde `OWASP ZAP` gibi araçlarla otomatize güvenlik testleri gerçekleştirilerek çalışma zamanı zafiyetleri tespit edilir.
* **Gizli Bilgi Yönetimi (Secrets Management):**
    * API anahtarları, veritabanı şifreleri gibi hassas bilgiler, kod tabanına gömülmek yerine ortam değişkenleri (environment variables) veya güvenli gizli bilgi yönetim sistemleri aracılığıyla yönetilir.

## 📂 Proje Yapısı

guvenli-not-defteri/
├── app.py                # Ana Flask uygulaması
├── requirements.txt      # Python bağımlılıkları
├── Dockerfile            # Docker imajı oluşturma talimatları
├── .dockerignore         # Docker build'de hariç tutulacak dosyalar
├── .gitignore            # Git tarafından izlenmeyecek dosyalar
├── static/               # CSS, JS, resim dosyaları
│   └── style.css
├── templates/            # HTML şablonları
│   ├── index.html
│   └── note.html
├── tests/                # Birim ve entegrasyon testleri
│   └── test_app.py
├── README.md             # Bu dosya
└── LICENSE               # Proje lisansı

*(Not: `tests/` klasörü iyi bir pratik olarak eklenmiştir, projede henüz bulunmuyorsa eklenebilir.)*

## 🤝 Katkıda Bulunma

Bu projeyi daha da geliştirmek ve DevSecOps pratiklerini zenginleştirmek için katkılarınızı bekliyoruz! Lütfen bir "issue" açarak fikirlerinizi paylaşın veya "pull request" göndererek doğrudan katkıda bulunun.

1.  Projeyi Fork'layın.
2.  Kendi branch'inizi oluşturun (`git checkout -b ozellik/yeni-ozellik`).
3.  Değişikliklerinizi commit'leyin (`git commit -am 'Yeni bir özellik eklendi'`).
4.  Branch'inizi push'layın (`git push origin ozellik/yeni-ozellik`).
5.  Bir Pull Request oluşturun.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.
