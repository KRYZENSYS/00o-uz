"""Authentication API: Email/Password, Telegram, OTP, 2FA"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, Field

from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
    generate_otp, generate_2fa_secret, verify_2fa, generate_2fa_qr
)
from app.models import User, UserRole, UserStatus

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=32)
    language: str = "uz"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    two_factor_code: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == int(payload.get("sub"))))
    user = result.scalar_one_or_none()
    if not user or user.status == UserStatus.BANNED:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where((User.email == data.email) | (User.username == data.username)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email or username already taken")

    user = User(
        email=data.email, username=data.username, full_name=data.full_name,
        hashed_password=hash_password(data.password), language=data.language,
        role=UserRole.USER, status=UserStatus.ACTIVE,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user={"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name, "role": user.role.value}
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.two_factor_enabled:
        if not data.two_factor_code or not verify_2fa(user.two_factor_secret, data.two_factor_code):
            raise HTTPException(status_code=401, detail="2FA code required")
    user.last_login_at = datetime.utcnow()
    await db.commit()
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user={"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name, "role": user.role.value}
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    result = await db.execute(select(User).where(User.id == int(payload.get("sub"))))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user={"id": user.id, "email": user.email, "username": user.username}
    )


@router.post("/telegram")
async def telegram_auth(id: int, first_name: str, last_name: str = None, username: str = None, photo_url: str = None, db: AsyncSession = Depends(get_db)):
    tg_id = str(id)
    result = await db.execute(select(User).where(User.telegram_username == tg_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email=f"tg_{tg_id}@00o.uz", username=f"tg_{username or tg_id}",
            full_name=f"{first_name} {last_name or ''}".strip(),
            telegram_username=tg_id, avatar=photo_url,
            role=UserRole.USER, status=UserStatus.ACTIVE, is_verified=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "user": {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name}
    }


@router.post("/otp/send")
async def send_otp(email: EmailStr):
    return {"message": "OTP sent", "code": generate_otp()}  # Implement Redis + email


@router.post("/2fa/setup")
async def setup_2fa(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = generate_2fa_secret()
    current_user.two_factor_secret = secret
    await db.commit()
    return {"secret": secret, "qr_code": f"data:image/png;base64,{generate_2fa_qr(current_user.email, secret)}"}


@router.post("/2fa/enable")
async def enable_2fa(code: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user.two_factor_secret or not verify_2fa(current_user.two_factor_secret, code):
        raise HTTPException(status_code=400, detail="Invalid code")
    current_user.two_factor_enabled = True
    await db.commit()
    return {"message": "2FA enabled"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id, "email": current_user.email, "username": current_user.username,
        "full_name": current_user.full_name, "role": current_user.role.value,
        "is_verified": current_user.is_verified, "language": current_user.language,
        "two_factor_enabled": current_user.two_factor_enabled
    }
