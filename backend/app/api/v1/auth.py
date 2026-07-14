"""Auth API - register, login, JWT, 2FA, OAuth"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import secrets
import pyotp

from app.core.database import get_db
from app.core.config import settings
from app.models import User, UserRole
from app.services.email import EmailService

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterReq(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)
    phone: Optional[str] = None


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class TelegramAuthReq(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int


class RefreshReq(BaseModel):
    refresh_token: str


class PasswordResetReq(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class TwoFactorReq(BaseModel):
    code: str


def create_token(user_id: int, token_type: str = "access") -> str:
    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    payload = {"sub": str(user_id), "type": token_type, "exp": expire, "iat": datetime.utcnow()}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(token: str = None, db: AsyncSession = Depends(get_db)) -> User:
    from fastapi import Header
    raise NotImplementedError("Use get_current_user dependency")


from fastapi import Header
async def get_current_user(authorization: Optional[str] = Header(None), db: AsyncSession = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401, "Token yo'q")
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError: raise HTTPException(401, "Token yaroqsiz")
    user = await db.get(User, user_id)
    if not user or not user.is_active: raise HTTPException(401, "Foydalanuvchi topilmadi yoki bloklangan")
    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.role not in [UserRole.ADMIN, UserRole.MODERATOR]: raise HTTPException(403, "Admin huquqi kerak")
    return user


@router.post("/register")
async def register(req: RegisterReq, db: AsyncSession = Depends(get_db)):
    # Check existing
    existing = await db.scalar(select(User).where((User.email == req.email) | (User.username == req.username)))
    if existing: raise HTTPException(400, "Email yoki username band")
    
    user = User(
        email=req.email, username=req.username, full_name=req.full_name,
        phone=req.phone, password_hash=pwd_context.hash(req.password),
        tokens=100, is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Send welcome email
    try: await EmailService.send_welcome(user.email, user.full_name)
    except: pass
    
    return {"id": user.id, "email": user.email, "username": user.username, "access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh"), "tokens": user.tokens}


@router.post("/login")
async def login(req: LoginReq, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == req.email))
    if not user or not pwd_context.verify(req.password, user.password_hash or ""): raise HTTPException(401, "Email yoki parol noto'g'ri")
    if not user.is_active: raise HTTPException(403, "Akkaunt bloklangan")
    if user.two_factor_enabled:
        return {"requires_2fa": True, "user_id": user.id}
    
    user.last_login = datetime.utcnow()
    await db.commit()
    
    return {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name, "is_premium": user.is_premium, "is_verified": user.is_verified, "role": user.role.value, "tokens": user.tokens, "avatar_url": user.avatar_url, "access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh")}


@router.post("/login/2fa")
async def login_2fa(req: TwoFactorReq, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user or not user.two_factor_enabled: raise HTTPException(400)
    totp = pyotp.TOTP(user.two_factor_secret)
    if not totp.verify(req.code): raise HTTPException(401, "Kod noto'g'ri")
    return {"access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh")}


@router.post("/telegram")
async def telegram_auth(req: TelegramAuthReq, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.telegram_id == req.id))
    if not user:
        user = User(
            telegram_id=req.id, email=f"tg_{req.id}@00o.uz",
            username=req.username or f"user{req.id}", full_name=req.first_name + (f" {req.last_name}" if req.last_name else ""),
            avatar_url=req.photo_url, is_verified=True, tokens=100
        )
        db.add(user); await db.commit(); await db.refresh(user)
    user.last_login = datetime.utcnow(); await db.commit()
    return {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name, "is_premium": user.is_premium, "is_verified": user.is_verified, "role": user.role.value, "tokens": user.tokens, "avatar_url": user.avatar_url, "access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh")}


@router.post("/refresh")
async def refresh(req: RefreshReq, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(req.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh": raise HTTPException(401, "Invalid token type")
        user = await db.get(User, int(payload.get("sub")))
        if not user: raise HTTPException(401)
        return {"access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh")}
    except JWTError: raise HTTPException(401, "Token yaroqsiz")


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name, "bio": user.bio, "phone": user.phone, "avatar_url": user.avatar_url, "is_premium": user.is_premium, "is_verified": user.is_verified, "role": user.role.value, "tokens": user.tokens, "premium_expires": user.premium_expires.isoformat() if user.premium_expires else None, "two_factor_enabled": user.two_factor_enabled, "created_at": user.created_at.isoformat()}


@router.post("/password/reset")
async def password_reset(req: PasswordResetReq, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == req.email))
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        await db.commit()
        try: await EmailService.send_password_reset(user.email, f"https://00o.uz/reset?token={token}")
        except: pass
    return {"message": "Agar email ro'yxatda bo'lsa, link yuborildi"}


@router.post("/password/reset/confirm")
async def password_reset_confirm(req: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.reset_token == req.token))
    if not user or user.reset_token_expires < datetime.utcnow(): raise HTTPException(400, "Token yaroqsiz yoki eskirgan")
    user.password_hash = pwd_context.hash(req.new_password)
    user.reset_token = None; user.reset_token_expires = None
    await db.commit()
    return {"message": "Parol o'zgartirildi"}


@router.post("/2fa/enable")
async def enable_2fa(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = pyotp.random_base32()
    user.two_factor_secret = secret
    user.two_factor_enabled = True
    await db.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="00o.uz")
    return {"secret": secret, "uri": uri, "message": "2FA yoqildi"}


@router.post("/2fa/disable")
async def disable_2fa(req: TwoFactorReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.two_factor_enabled: raise HTTPException(400)
    totp = pyotp.TOTP(user.two_factor_secret)
    if not totp.verify(req.code): raise HTTPException(401, "Kod noto'g'ri")
    user.two_factor_enabled = False
    user.two_factor_secret = None
    await db.commit()
    return {"message": "2FA o'chirildi"}
