"""Security utilities"""
from datetime import datetime, timedelta
from typing import Optional
import secrets
import pyotp
import qrcode
from io import BytesIO
import base64
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"exp": expire, "sub": str(subject), "type": "access"},
                     settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"exp": expire, "sub": str(subject), "type": "refresh"},
                     settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def generate_otp(length: int = 6) -> str:
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])


def generate_2fa_secret() -> str:
    return pyotp.random_base32()


def verify_2fa(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code)


def generate_2fa_qr(username: str, secret: str) -> str:
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="00o.uz")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def generate_referral_code(length: int = 8) -> str:
    return secrets.token_urlsafe(length)[:length].upper()
