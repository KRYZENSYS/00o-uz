"""Auth - Register, Login, OAuth, 2FA"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
import pyotp, qrcode, io, base64, secrets, hashlib, hmac
from typing import Optional

from app.core.config import settings
from app.core.database import get_db
from app.models import User, UserRole
from app.services.email import EmailService

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    username: str = Field(..., min_length=3, max_length=32)
    full_name: str
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    email_or_username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


def create_token(user_id: int, type: str = "access") -> str:
    expire = datetime.utcnow() + timedelta(days=7 if type == "refresh" else 1)
    return jwt.encode({"user_id": user_id, "type": type, "exp": expire}, settings.SECRET_KEY, algorithm="HS256")


async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(creds.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id: raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = await db.get(User, user_id)
    if not user or not user.is_active: raise HTTPException(401, "User not found")
    return user


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(or_(User.email == req.email, User.username == req.username)))
    if existing.scalar_one_or_none(): raise HTTPException(400, "Email yoki username band")
    user = User(email=req.email, phone=req.phone, username=req.username, full_name=req.full_name,
                password_hash=pwd_context.hash(req.password), tokens=50)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return TokenResponse(access_token=create_token(user.id), refresh_token=create_token(user.id, "refresh"),
                         user={"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name})


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(or_(User.email == req.email_or_username, User.username == req.email_or_username)))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(req.password, user.password_hash): raise HTTPException(401, "Noto'g'ri login yoki parol")
    if not user.is_active: raise HTTPException(403, "Bloklangan")
    user.last_login = datetime.utcnow()
    await db.commit()
    return TokenResponse(access_token=create_token(user.id), refresh_token=create_token(user.id, "refresh"),
                         user={"id": user.id, "email": user.email, "username": user.username, "is_premium": user.is_premium})


@router.post("/telegram", response_model=TokenResponse)
async def telegram_auth(data: dict, db: AsyncSession = Depends(get_db)):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    check = f"{data['id']}\n{data.get('first_name','')}\n{data.get('last_name','')}\n{data.get('username','')}\n{data.get('photo_url','')}\n{data['auth_date']}"
    h = hmac.new(hashlib.sha256(bot_token.encode()).digest(), check.encode(), hashlib.sha256).hexdigest()
    if h != data.get("hash"): raise HTTPException(401, "Invalid")
    result = await db.execute(select(User).where(User.telegram_id == data["id"]))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=data["id"], username=data.get("username") or f"u{data['id']}",
                    full_name=data.get("first_name", ""), email=f"tg{data['id']}@00o.uz", password_hash="", tokens=50)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return TokenResponse(access_token=create_token(user.id), refresh_token=create_token(user.id, "refresh"),
                         user={"id": user.id, "username": user.username, "full_name": user.full_name})


@router.post("/2fa/enable")
async def enable_2fa(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = pyotp.random_base32()
    user.two_factor_secret = secret
    await db.commit()
    uri = pyotp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="00o.uz")
    qr = qrcode.make(uri); buf = io.BytesIO(); qr.save(buf, format="PNG")
    return {"secret": secret, "qr": f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"}


@router.post("/forgot-password")
async def forgot(email: EmailStr, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        user.reset_token = secrets.token_urlsafe(32)
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        await db.commit()
    return {"message": "Xabar yuborildi"}


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name,
            "avatar": user.avatar_url, "is_premium": user.is_premium, "tokens": user.tokens, "role": user.role.value}
