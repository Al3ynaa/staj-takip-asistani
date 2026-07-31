# Staj Takip Asistanı

Staj başvurularını takip etmek, yönetmek ve yapay zeka desteğiyle, ilana özel ön yazı üretmek için geliştirilmiş, tam kapsamlı bir web uygulaması.

## Özellikler

- Kullanıcı kayıt/giriş sistemi (JWT tabanlı kimlik doğrulama)
- Staj başvurularını ekleme, listeleme, güncelleme, silme (CRUD)
- Claude AI entegrasyonu ile, ilana özel ön yazı üretimi
- Kullanıcı profili (CV bilgisi) yönetimi
- React tabanlı, modern kullanıcı arayüzü
- Docker ve PostgreSQL ile, production-ready altyapı

## Kullanılan Teknolojiler

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, JWT, Anthropic Claude API
**Frontend:** React, React Router
**DevOps:** Docker, Docker Compose

## Kurulum

```bash
docker compose up
```

Backend, `http://localhost:8000` adresinde çalışır.
## Ekran Görüntüleri

### Giriş Sayfası
![Giriş Sayfası](screenshots/01-giris.png)

### Başvurular Sayfası
![Başvurular Sayfası](screenshots/02-basvurular.png)

### Profilim Sayfası
![Profilim Sayfası](screenshots/03-profilim.png)

### İlan Metni Girme
![İlan Metni](screenshots/04-ilan-metni.png)

### Üretilen Ön Yazı
![Ön Yazı Sonucu](screenshots/05-on-yazi-sonuc.png)
