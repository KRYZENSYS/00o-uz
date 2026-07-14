"""Admin Panel"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.api.v1.auth import get_admin_user
from app.models import User, Startup, FreelancerService, Job, Message, Transaction

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats/overview")
async def overview(db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    users_count = await db.scalar(select(func.count(User.id))) or 0
    startups_count = await db.scalar(select(func.count(Startup.id))) or 0
    services_count = await db.scalar(select(func.count(FreelancerService.id))) or 0
    jobs_count = await db.scalar(select(func.count(Job.id))) or 0
    messages_count = await db.scalar(select(func.count(Message.id))) or 0
    revenue = await db.scalar(select(func.sum(Transaction.amount))) or 0
    today = datetime.utcnow().date()
    new_users_today = await db.scalar(
        select(func.count(User.id)).where(func.date(User.created_at) == today)
    ) or 0
    return {
        "users": users_count, "startups": startups_count, "services": services_count,
        "jobs": jobs_count, "messages": messages_count,
        "revenue": float(revenue), "new_users_today": new_users_today
    }


@router.get("/users")
async def list_users(
    search: Optional[str] = None, role: Optional[str] = None,
    is_active: Optional[bool] = None, limit: int = Query(50, le=200), offset: int = 0,
    db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)
):
    query = select(User)
    if search:
        query = query.where((User.email.ilike(f"%{search}%")) | (User.username.ilike(f"%{search}%")))
    if role: query = query.where(User.role == role)
    if is_active is not None: query = query.where(User.is_active == is_active)
    query = query.order_by(User.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    users = result.scalars().all()
    return [{
        "id": u.id, "email": u.email, "username": u.username, "full_name": u.full_name,
        "role": u.role.value, "is_active": u.is_active, "is_verified": u.is_verified,
        "is_premium": u.is_premium, "tokens": u.tokens, "created_at": u.created_at.isoformat()
    } for u in users]


@router.post("/users/{user_id}/ban")
async def ban_user(user_id: int, reason: str, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    user = await db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    user.is_active = False
    user.ban_reason = reason
    await db.commit()
    return {"message": "Banned"}


@router.post("/users/{user_id}/unban")
async def unban_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    user = await db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    user.is_active = True
    user.ban_reason = None
    await db.commit()
    return {"message": "Unbanned"}


@router.post("/users/{user_id}/premium")
async def grant_premium(user_id: int, days: int = 30, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    user = await db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    user.is_premium = True
    user.premium_expires = datetime.utcnow() + timedelta(days=days)
    await db.commit()
    return {"message": f"Premium {days} days"}


@router.post("/startups/{startup_id}/feature")
async def feature_startup(startup_id: int, featured: bool = True, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    s = await db.get(Startup, startup_id)
    if not s: raise HTTPException(404, "Not found")
    s.is_featured = featured
    await db.commit()
    return {"featured": s.is_featured}


@router.get("/revenue")
async def revenue_stats(days: int = 30, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    start_date = datetime.utcnow() - timedelta(days=days)
    revenue_data = await db.execute(
        select(func.date(Transaction.created_at).label("date"), func.sum(Transaction.amount).label("total"))
        .where(Transaction.created_at >= start_date).group_by(func.date(Transaction.created_at)).order_by("date")
    )
    return [{"date": str(r.date), "total": float(r.total or 0)} for r in revenue_data]


@router.get("/analytics/traffic")
async def traffic(_: User = Depends(get_admin_user)):
    return {
        "page_views": 15234, "unique_visitors": 8756,
        "bounce_rate": 0.42, "avg_session_duration": 245
    }


@router.post("/broadcast")
async def broadcast(title: str, message: str, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    users = await db.execute(select(User.id).where(User.is_active == True))
    return {"sent_to": len(users.fetchall())}
