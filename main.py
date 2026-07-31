from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
import schemas
import auth
import ai_servis


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def anasayfa():
    return {"mesaj": "Merhaba Çalışıyor!"}

@app.post("/basvurular", response_model=schemas.BasvuruGoster)
def basvuru_ekle(basvuru: schemas.BasvuruOlustur, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    yeni_basvuru = models.Basvuru(**basvuru.dict(), kullanici_id=current_user.id)
    db.add(yeni_basvuru)
    db.commit()
    db.refresh(yeni_basvuru)
    return yeni_basvuru

@app.get("/basvurular", response_model=list[schemas.BasvuruGoster])
def basvuru_goster(db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    return db.query(models.Basvuru).filter(models.Basvuru.kullanici_id == current_user.id).all()

@app.get("/basvurular/{basvuru_id}", response_model=schemas.BasvuruGoster)
def basvuru_getir(basvuru_id: int, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    basvuru = db.query(models.Basvuru).filter(models.Basvuru.id == basvuru_id, models.Basvuru.kullanici_id == current_user.id).first()
    if basvuru is None:
        raise HTTPException(status_code=404, detail="Başvuru Bulunamadı")
    return basvuru

@app.put("/basvurular/{basvuru_id}", response_model=schemas.BasvuruGoster)
def basvuru_guncelle(basvuru_id: int, guncel_bilgi: schemas.BasvuruOlustur, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    basvuru = db.query(models.Basvuru).filter(models.Basvuru.id == basvuru_id, models.Basvuru.kullanici_id == current_user.id).first()
    if basvuru is None:
        raise HTTPException(status_code=404, detail="Başvuru bulunamadı")
    basvuru.sirket = guncel_bilgi.sirket
    basvuru.pozisyon = guncel_bilgi.pozisyon
    basvuru.tarih = guncel_bilgi.tarih
    basvuru.durum = guncel_bilgi.durum
    basvuru.not_alani = guncel_bilgi.not_alani
    db.commit()
    db.refresh(basvuru)
    return basvuru

@app.delete("/basvurular/{basvuru_id}")
def basvuru_sil(basvuru_id: int, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    basvuru = db.query(models.Basvuru).filter(models.Basvuru.id == basvuru_id, models.Basvuru.kullanici_id == current_user.id).first()
    if basvuru is None:
        raise HTTPException(status_code=404, detail="Başvuru Bulunamadı")
    db.delete(basvuru)
    db.commit()
    return {"mesaj": "Başvuru silindi"}

@app.post("/kayit")
def kayit_ol(kullanici: schemas.KullaniciOlustur, db: Session = Depends(get_db)):
    hash_sifre = auth.sifre_hashle(kullanici.sifre)
    yeni_kullanici = models.Kullanici(email=kullanici.email, sifre_hash=hash_sifre)
    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)
    return {"mesaj": "Kayıt başarılı", "email": yeni_kullanici.email}

@app.post("/giris")
def giris_yap(bilgi: schemas.GirisBilgisi, db: Session = Depends(get_db)):
    kullanici = db.query(models.Kullanici).filter(models.Kullanici.email == bilgi.email).first()
    if kullanici is None:
        raise HTTPException(status_code=401, detail="Email veya şifre yanlış")
    if not auth.sifre_dogrula(bilgi.sifre, kullanici.sifre_hash):
        raise HTTPException(status_code=401, detail="Email veya şifre yanlış")
    token = auth.token_uret(kullanici.email)
    return {"access_token": token, "token_type": "bearer"}

@app.put("/profil")
def profil_guncelle(profil: schemas.ProfilGuncelle, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    kullanici = db.query(models.Kullanici).filter(models.Kullanici.email == current_user.email).first()
    kullanici.profil_bilgisi = profil.profil_bilgisi
    db.commit()
    db.refresh(kullanici)
    return {"mesaj": "Profil güncellendi", "profil_bilgisi": kullanici.profil_bilgisi}

@app.post("/basvurular/{basvuru_id}/on-yazi")
def on_yazi_olustur(basvuru_id: int, istek: schemas.OnYaziIstek, db: Session = Depends(get_db), current_user: models.Kullanici = Depends(auth.get_current_user)):
    basvuru = db.query(models.Basvuru).filter(models.Basvuru.id == basvuru_id, models.Basvuru.kullanici_id == current_user.id).first()
    if basvuru is None:
        raise HTTPException(status_code=404, detail="Başvuru bulunamadı")

    profil = current_user.profil_bilgisi or "Belirtilmedi"
    on_yazi = ai_servis.on_yazi_uret(istek.ilan_metni, profil)
    return {"on_yazi": on_yazi}
