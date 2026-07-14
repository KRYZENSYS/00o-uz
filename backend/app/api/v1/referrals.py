"""Referral API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Referral

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.get("/stats")
async def my_stats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(Referral.id)).where(Referral.referrer_id == user.id)) or 0
    rewarded = await db.scalar(select(func.count(Referral.id)).where(Referral.referrer_id == user.id, Referral.reward_given == True)) or 0
    return {
        "total_referrals": total, "rewarded": rewarded, "pending": total - rewarded,
        "tokens_earned": rewarded * 50, "link": f"https://t.me/oo0o_uz_bot?start=ref_{user.id}"
    }


@router.get("/list")
async def my_referrals(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Referral, User).join(User, User.id == Referral.referred_id)
        .where(Referral.referrer_id == user.id).order_by(Referral.created_at.desc())
    )
    return [{"id": ref.id, "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url}, "reward_given": ref.reward_given, "created_at": ref.created_at.isoformat()} for ref, u in r.all()]


@router.post("/apply/{code}")
async def apply_code(code: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Apply referral code"""
    try:
        referrer_id = int(code.replace("ref_", ""))
    except: raise HTTPException(400, "Invalid code")
    
    if referrer_id == user.id: raise HTTPException(400, "O'zingizni taklif qila olmaysiz")
    referrer = await db.get(User, referrer_id)
    if not referrer: raise HTTPException(404, "Referrer not found")
    
    # Check if already referred
    existing = await db.scalar(select(Referral).where(Referral.referred_id == user.id))
    if existing: raise HTTPException(400, "Siz allaqachon taklif qilingansiz")
    
    ref = Referral(referrer_id=referrer_id, referred_id=user.id, reward_given=True)
    db.add(ref)
    
    # Give rewards
    referrer.tokens += 50
    user.tokens += 50
    
    await db.commit()
    return {"message": "Referral code qabul qilindi", "tokens_received": 50}
