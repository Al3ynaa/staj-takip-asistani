from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt

sifre_araci= CryptContext(schemes=["bcrypt"],deprecated="auto")

def sifre_hashle(sifre:str)->str:
	return sifre_araci.hash(sifre)

def sifre_dogrula(girilen_sifre:str, hash_sifre:str) -> bool:
	return sifre_araci.verify(girilen_sifre, hash_sifre)

GIZLI_ANAHTAR="bu-çok-gizli-bir-anahtar-değiştirilmeli"
ALGORITMA="HS256"
TOKEN_SURESI_DAKIKA=60

def token_uret(email:str)->str:
	veri={"sub": email, "exp": datetime.utcnow()+timedelta(minutes=TOKEN_SURESI_DAKIKA)}
	return jwt.encode(veri, GIZLI_ANAHTAR,algorithm=ALGORITMA)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="giris")

def get_db():
	db=SessionLocal()
	try:
		yield db
	finally:
		db.close()

def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
	hata=HTTPException(status_code=401,detail="Geçersiz kimlik bilgisi")
	try:
		veri=jwt.decode(token,GIZLI_ANAHTAR,algorithms=[ALGORITMA])
		email=veri.get("sub")
		if email is None:
			raise hata
	except JWTError:

		raise hata
	kullanici=db.query(models.Kullanici).filter(models.Kullanici.email==email).first()
	if kullanici is None:
		raise hata
	return kullanici
