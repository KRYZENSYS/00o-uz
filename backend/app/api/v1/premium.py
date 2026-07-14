"""Premium API - subscription management"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Transaction
from app.services.payments import process_payment, PaymentRequest, activate_premium

router = APIRouter(prefix="/premium", tags=["premium"])


class SubscribeReq(BaseModel):
    plan: str  # month, year, lifetime
    method: str  # payme, click, uzum, stripe, ton


@router.post("/subscribe")
async def subscribe(req: SubscribeReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plans = {"month": (49000, 30), "year": (490000, 365), "lifetime": (1999000, 36500)}
    if req.plan not in plans: raise HTTPException(400, "Invalid plan")
    price, days = plans[req.plan]
    
    # Create payment
    pay = await process_payment(PaymentRequest(amount=price, currency="UZS", method=req.method, user_id=user.id, description=f"Premium {req.plan}"))
    
    # Create transaction record
    tx = Transaction(user_id=user.id, type="premium", amount=price, currency="UZS", method=req.method, status="pending", description=f"Premium {req.plan}")
    db.add(tx)
    await db.commit()
    
    return {"transaction_id": tx.id, "payment": pay, "amount": price, "days": days, "plan": req.plan}


@router.post("/verify/{tx_id}")
async def verify(tx_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Verify payment and activate premium (called after payment)"""
    tx = await db.get(Transaction, tx_id)
    if not tx or tx.user_id != user.id: raise HTTPException(404)
    
    plans = {"month": 30, "year": 365, "lifetime": 36500}
    days = plans.get(req.plan if hasattr(req, 'plan') else "month", 30)
    
    tx.status = "completed"
    activate_premium(user, days)
    await db.commit()
    
    return {"message": "Premium faollashtirildi", "expires": user.premium_expires.isoformat()}


@router.get("/status")
async def status(user: User = Depends(get_current_user)):
    active = user.is_premium and user.premium_expires and user.premium_expires > datetime.utcnow()
    return {
        "is_premium": user.is_premium,
        "active": active,
        "expires": user.premium_expires.isoformat() if user.premium_expires else None,
        "tokens": user.tokens,
        "plan": "lifetime" if user.premium_expires and (user.premium_expires - datetime.utcnow()).days > 3650 else 
                "year" if user.premium_expires and (user.premium_expires - datetime.utcnow()).days > 30 else
                "month" if active else None
    }


@router.post("/cancel")
async def cancel(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.is_premium = False
    await db.commit()
    return {"message": "Premium bekor qilindi"}


@router.get("/transactions")
async def my_transactions(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Transaction).where(Transaction.user_id == user.id).order_by(Transaction.created_at.desc()).limit(50))
    return [{"id": t.id, "type": t.type, "amount": t.amount, "currency": t.currency, "method": t.method, "status": t.status, "description": t.description, "created_at": t.created_at.isoformat()} for t in r.scalars().all()]
