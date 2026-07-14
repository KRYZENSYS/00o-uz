"""KYC, Phone verification, Biometric, Security"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import secrets, os, shutil

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, KYCDocument, Device, LoginHistory, SecurityLog

router = APIRouter(prefix="/security", tags=["security"])


class PhoneReq(BaseModel):
    phone: str


class VerifyCodeReq(BaseModel):
    code: str


# ============ PHONE VERIFICATION ============
@router.post("/phone/send-code")
async def send_phone_code(req: PhoneReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Send SMS verification code"""
    code = str(secrets.randbelow(900000) + 100000)
    user.phone = req.phone
    user.phone_verification_code = code
    user.phone_verification_expires = datetime.utcnow().replace(microsecond=0) + __import__('datetime').timedelta(minutes=10)
    await db.commit()
    # In production: integrate with SMS service (Eskiz, Playmobile)
    return {"message": f"Kod yuborildi: {code}", "phone": req.phone, "demo": True}


@router.post("/phone/verify")
async def verify_phone(req: VerifyCodeReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.phone_verification_code or user.phone_verification_code != req.code: raise HTTPException(400, "Kod noto'g'ri")
    if user.phone_verification_expires and user.phone_verification_expires < datetime.utcnow(): raise HTTPException(400, "Kod eskirgan")
    user.is_phone_verified = True
    user.phone_verification_code = None
    user.phone_verification_expires = None
    await db.commit()
    return {"message": "Telefon tasdiqlandi"}


# ============ EMAIL VERIFICATION ============
@router.post("/email/send-code")
async def send_email_code(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    code = str(secrets.randbelow(900000) + 100000)
    user.email_verification_code = code
    user.email_verification_expires = datetime.utcnow() + __import__('datetime').timedelta(hours=24)
    await db.commit()
    # In production: send email
    return {"message": f"Email kod: {code}", "demo": True}


@router.post("/email/verify")
async def verify_email(req: VerifyCodeReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.email_verification_code or user.email_verification_code != req.code: raise HTTPException(400, "Kod noto'g'ri")
    user.is_email_verified = True
    user.is_verified = True
    user.email_verification_code = None
    await db.commit()
    return {"message": "Email tasdiqlandi"}


# ============ KYC (Identity Verification) ============
@router.post("/kyc/upload")
async def upload_kyc_doc(doc_type: str, file: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Upload KYC document (passport, ID card, selfie)"""
    if doc_type not in ["passport", "id_card", "selfie", "driver_license"]: raise HTTPException(400, "Noto'g'ri hujjat turi")
    if user.kyc_status == "approved": raise HTTPException(400, "Allaqachon tasdiqlangan")
    
    os.makedirs("uploads/kyc", exist_ok=True)
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    fname = f"{user.id}_{secrets.token_urlsafe(8)}.{ext}"
    path = f"uploads/kyc/{fname}"
    with open(path, "wb") as f: shutil.copyfileobj(file.file, f)
    
    doc = KYCDocument(user_id=user.id, doc_type=doc_type, file_url=f"/uploads/kyc/{fname}", status="pending")
    db.add(doc)
    user.kyc_status = "in_review"
    await db.commit()
    return {"id": doc.id, "status": "pending"}


@router.get("/kyc/my")
async def my_kyc(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(KYCDocument).where(KYCDocument.user_id == user.id))
    return [{"id": d.id, "type": d.doc_type, "file_url": d.file_url, "status": d.status, "created_at": d.created_at.isoformat()} for d in r.scalars().all()]


@router.post("/kyc/admin/{user_id}/approve")
async def approve_kyc(user_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ["admin", "moderator"]: raise HTTPException(403)
    target = await db.get(User, user_id)
    if not target: raise HTTPException(404)
    target.kyc_status = "approved"
    target.is_verified = True
    await db.commit()
    return {"message": "Tasdiqlandi"}


# ============ DEVICES MANAGEMENT ============
@router.get("/devices")
async def my_devices(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Device).where(Device.user_id == user.id, Device.is_active == True).order_by(Device.last_used.desc()))
    return [{"id": d.id, "name": d.name, "type": d.type, "ip": d.ip, "location": d.location, "last_used": d.last_used.isoformat(), "is_current": d.is_current} for d in r.scalars().all()]


@router.delete("/devices/{device_id}")
async def remove_device(device_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = await db.get(Device, device_id)
    if not d or d.user_id != user.id: raise HTTPException(404)
    d.is_active = False
    await db.commit()
    return {"message": "O'chirildi"}


@router.post("/devices/logout-all")
async def logout_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(Device.__table__.update().where(Device.user_id == user.id).values(is_active=False))
    await db.commit()
    return {"message": "Barcha qurilmalardan chiqildi"}


# ============ LOGIN HISTORY ============
@router.get("/login-history")
async def login_history(limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(LoginHistory).where(LoginHistory.user_id == user.id).order_by(LoginHistory.created_at.desc()).limit(limit))
    return [{"id": h.id, "ip": h.ip, "user_agent": h.user_agent, "location": h.location, "status": h.status, "created_at": h.created_at.isoformat()} for h in r.scalars().all()]


# ============ SECURITY LOGS ============
@router.get("/logs")
async def security_logs(limit: int = 100, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(SecurityLog).where(SecurityLog.user_id == user.id).order_by(SecurityLog.created_at.desc()).limit(limit))
    return [{"id": l.id, "event": l.event, "ip": l.ip, "location": l.location, "created_at": l.created_at.isoformat()} for l in r.scalars().all()]


# ============ BIOMETRIC =============
@router.post("/biometric/enable")
async def enable_biometric(public_key: str, device_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Enable WebAuthn/biometric login"""
    user.biometric_public_key = public_key
    user.biometric_device_id = device_id
    await db.commit()
    return {"message": "Biometrik login yoqildi"}


@router.post("/biometric/auth")
async def biometric_auth(signature: str, challenge: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Authenticate with biometric"""
    if not user.biometric_public_key: raise HTTPException(400, "Biometrik login yoqilmagan")
    # In production: verify WebAuthn signature
    from app.api.v1.auth import create_token
    return {"access_token": create_token(user.id), "refresh_token": create_token(user.id, "refresh")}


# ============ BLOCK USER =============
@router.post("/block/{user_id}")
async def block_user(user_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import Block
    existing = await db.scalar(select(Block).where(Block.user_id == user.id, Block.blocked_id == user_id))
    if existing: return {"message": "Allaqachon bloklagansiz"}
    db.add(Block(user_id=user.id, blocked_id=user_id))
    await db.commit()
    return {"message": "Bloklandi"}


@router.post("/unblock/{user_id}")
async def unblock_user(user_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import Block
    b = await db.scalar(select(Block).where(Block.user_id == user.id, Block.blocked_id == user_id))
    if b: await db.delete(b); await db.commit()
    return {"message": "Blokdan chiqarildi"}


@router.get("/blocked")
async def blocked_users(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import Block, User
    r = await db.execute(select(Block, User).join(User, User.id == Block.blocked_id).where(Block.user_id == user.id))
    return [{"id": b.id, "user": {"id": u.id, "full_name": u.full_name, "username": u.username, "avatar_url": u.avatar_url}} for b, u in r.all()]


# ============ REPORT USER ============
@router.post("/report/{user_id}")
async def report_user(user_id: int, reason: str, description: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import Report
    r = Report(reporter_id=user.id, reported_id=user_id, reason=reason, description=description, status="pending")
    db.add(r); await db.commit()
    return {"message": "Shikoyat qabul qilindi"}


# ============ NSFW IMAGE DETECTION (simulated) ============
@router.post("/moderate/image")
async def moderate_image(image_url: str, user: User = Depends(get_current_user)):
    """Check image for NSFW content (in production: use ML model)"""
    return {"safe": True, "score": 0.02, "labels": ["safe"]}
