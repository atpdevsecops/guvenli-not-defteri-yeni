# 1. Temel imaj olarak Python 3.10'un slim (hafif) versiyonunu kullan
FROM python:3.10-slim

# 2. İşletim sistemi paketlerini güncelle ve gereksiz dosyaları temizle
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 3. pip, setuptools ve wheel'i güncelle
RUN python -m pip install --upgrade pip setuptools wheel

# YENİ: Güvenlik için root olmayan bir kullanıcı (appuser) ve grup (appgroup) oluştur.
# -r: Sistem kullanıcısı/grubu oluşturur (genellikle home dizini oluşturulmaz).
# --no-log-init: Debian tabanlı sistemlerde login.defs ile ilgili olası uyarıları/hataları engeller.
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# 4. Çalışma dizinini /app olarak ayarlaC:\Users\atpek\Desktop\Projects\guvenli-not-defteri
WORKDIR /app

# 5. requirements.txt dosyasını çalışma dizinine kopyala
# Bu ve sonraki COPY komutu root kullanıcısı bağlamında çalışır.
COPY requirements.txt ./

# 6. requirements.txt dosyasındaki Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# 7. Proje dosyalarının geri kalanını (örn: app.py) çalışma dizinine kopyala
COPY . .

# YENİ: /app dizininin ve içindeki tüm dosyaların sahipliğini oluşturduğumuz appuser:appgroup ikilisine ver.
# Bu adım, dosyalar kopyalandıktan SONRA yapılmalı ki doğru sahiplik atansın.
RUN chown -R appuser:appgroup /app

# YENİ: Root olmayan 'appuser' kullanıcısına geçiş yap.
# Bu satırdan sonraki tüm komutlar (örn: CMD) appuser bağlamında çalışacaktır.
USER appuser

# 8. Flask uygulamasının çalışacağı portu belirt (varsayılan Flask portu 5000)
# Bu satır USER komutundan önce veya sonra olabilir, işlevsel olarak büyük bir fark yaratmaz.
EXPOSE 5000

# 9. Konteyner başladığında uygulamayı çalıştıracak komut
# Bu komut artık 'appuser' olarak çalıştırılacak.
CMD ["python", "app.py"]