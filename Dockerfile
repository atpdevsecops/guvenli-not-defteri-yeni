# Dockerfile
# 1. Temel imaj olarak Python 3.10'un slim (hafif) versiyonunu kullan
FROM python:3.10-slim

# Ortam değişkenlerini ayarla (pip'in gereksiz loglarını engelle, Python'u optimize et)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 2. İşletim sistemi paketlerini güncelle, gunicorn ve diğer olası bağımlılıklar için gerekli build araçlarını kur
# ve gereksiz dosyaları temizle
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev musl-dev && \
    # gcc libffi-dev musl-dev bazı python paketlerinin (örn: cryptography) derlenmesi için gerekebilir
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 3. pip, setuptools ve wheel'i güncelle
RUN python -m pip install --upgrade pip setuptools wheel

# 4. Güvenlik için root olmayan bir kullanıcı (appuser) ve grup (appgroup) oluştur.
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# 5. Çalışma dizinini /app olarak ayarla
WORKDIR /app

# 6. requirements.txt dosyasını çalışma dizinine kopyala
# Bu katmanın önbelleğe alınması için uygulama kodundan önce kopyalanır.
COPY requirements.txt ./

# 7. requirements.txt dosyasındaki Python bağımlılıklarını yükle
# --no-cache-dir imaj boyutunu küçültür.
# Sanal ortam kullanmıyoruz çünkü konteyner zaten izole bir ortam.
RUN pip install --no-cache-dir -r requirements.txt

# 8. Proje dosyalarının geri kalanını (örn: app.py, templates klasörü) çalışma dizinine kopyala
COPY . .

# 9. /app dizininin ve içindeki tüm dosyaların sahipliğini oluşturduğumuz appuser:appgroup ikilisine ver.
RUN chown -R appuser:appgroup /app

# 10. Root olmayan 'appuser' kullanıcısına geçiş yap.
USER appuser

# 11. Flask uygulamasının çalışacağı portu belirt
EXPOSE 5000

# 12. Konteynerin sağlıklı olup olmadığını kontrol etmek için HEALTHCHECK (isteğe bağlı ama önerilir)
# Bu örnek, uygulamanın ana sayfasının 5 saniye içinde yanıt verip vermediğini kontrol eder.
# Gerçek uygulamanızda özel bir /health endpoint'i oluşturmak daha iyidir.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
  # Eğer uygulamanızda /health endpoint'i varsa: CMD curl -f http://localhost:5000/health || exit 1

# 13. Konteyner başladığında uygulamayı Gunicorn ile çalıştıracak komut
# Bu komut 'appuser' olarak çalıştırılacak.
# app:app -> app.py dosyasındaki 'app' adlı Flask nesnesi.
# requirements.txt dosyanızda 'gunicorn' olduğundan emin olun.
CMD ["gunicorn", "--workers", "2", "--threads", "2", "--worker-class", "gthread", "--bind", "0.0.0.0:5000", "app:app"]