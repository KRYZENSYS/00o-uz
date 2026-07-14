"""Admin API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.v1.auth import get_admin_user
from app.models import User, Startup, Job, FreelancerService, Notification, AIRequest, Transaction

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats/overview")
async def overview(user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    users = await db.scalar(select(func.count(User.id))) or 0
    startups = await db.scalar(select(func.count(Startup.id))) or 0
    jobs = await db.scalar(select(func.count(Job.id))) or 0
    services = await db.scalar(select(func.count(FreelancerService.id))) or 0
    notifs = await db.scalar(select(func.count(Notification.id))) or 0
    new_users = await db.scalar(select(func.count(User.id)).where(User.created_at >= datetime.utcnow() - timedelta(days=1))) or 0
    revenue = await db.scalar(select(func.sum(Transaction.amount)).where(Transaction.status == "completed")) or 0
    return {"users": users, "startups": startups, "jobs": jobs, "services": services, "messages": notifs, "new_users_today": new_users, "revenue": revenue}


@router.get("/users")
async def list_users(skip: int = 0, limit: int = 50, user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(User).order_by(User.created_at.desc()).offset(skip).limit(limit))
    return [{"id": u.id, "email": u.email, "username": u.username, "role": u.role.value, "is_active": u.is_active, "is_premium": u.is_premium, "tokens": u.tokens, "created_at": u.created_at.isoformat()} for u in r.scalars().all()]


@router.post("/users/{uid}/ban")
async def ban_user(uid: int, reason: str, user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    u = await db.get(User, uid)
    if not u: raise HTTPException(404)
    u.is_active = False; u.ban_reason = reason; await db.commit()
    return {"message": "Bloklandi"}


@router.post("/users/{uid}/unban")
async def unban_user(uid: int, user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    u = await db.get(User, uid)
    if not u: raise HTTPException(404)
    u.is_active = True; u.ban_reason = None; await db.commit()
    return {"message": "Blokdan chiqarildi"}


@router.post("/users/{uid}/premium")
async def grant_premium(uid: int, days: int = 30, user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    u = await db.get(User, uid)
    if not u: raise HTTPException(404)
    u.is_premium = True
    u.premium_expires = datetime.utcnow() + timedelta(days=days)
    await db.commit()
    return {"message": f"Premium {days} kun faollashtirildi"}


@router.get("/ai/usage")
async def ai_usage(user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(AIRequest.tool, func.count(AIRequest.id), func.sum(AIRequest.tokens_used)).group_by(AIRequest.tool))
    return [{"tool": t, "count": c, "tokens": tk or 0} for t, c, tk in r.all()]
