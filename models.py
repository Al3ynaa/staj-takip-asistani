from sqlalchemy import Column, Integer, String, Date,ForeignKey
from database import Base

class Basvuru(Base):
    __tablename__ = "basvurular"

    id = Column(Integer, primary_key=True, index=True)
    sirket = Column(String, nullable=False)
    pozisyon = Column(String, nullable=False)
    tarih = Column(Date, nullable=False)
    durum = Column(String, default="başvuruldu")
    not_alani = Column(String, nullable=True)
    kullanici_id=Column(Integer,ForeignKey("kullanicilar.id"))

class Kullanici(Base):
	__tablename__="kullanicilar"
	
	id = Column(Integer,primary_key=True, index=True)
	email=Column(String, unique=True,nullable=False)
	sifre_hash=Column(String,nullable=False)
	profil_bilgisi=Column(String,nullable=True)
