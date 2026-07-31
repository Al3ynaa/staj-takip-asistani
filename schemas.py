from pydantic import BaseModel
from datetime import date

class BasvuruOlustur(BaseModel):
    sirket: str
    pozisyon: str
    tarih: date
    durum: str = "başvuruldu"
    not_alani: str | None = None

class BasvuruGoster(BasvuruOlustur):
    id: int
    kullanici_id:int

    class Config:
        from_attributes = True

class KullaniciOlustur(BaseModel):
	email:str
	sifre:str

class GirisBilgisi(BaseModel):
	email:str
	sifre:str

class ProfilGuncelle(BaseModel):
	profil_bilgisi:str

class OnYaziIstek(BaseModel):
	ilan_metni:str
