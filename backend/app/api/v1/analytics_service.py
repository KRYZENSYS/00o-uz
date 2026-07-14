"""Analytics API - events, tracking"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_admin_user
from app.models import User, Analytics, Startup, Job, FreelancerService, AIRequest

router = APIRouter(prefix="/analytics", tags=["analytics"])


class EventTrack(BaseModel):
    event: str
    data: Optional[Dict[str, Any]] = None


@router.post("/track")
async def track(req: EventTrack, request: Request, user: User = Depends(get_current_user) if False else None, db: AsyncSession = Depends(get_db)):
    """Track event (public endpoint with optional user)"""
    e = Analytics(
        event=req.event, data=req.data or {},
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", "")[:500]
    )
    db.add(e)
    await db.commit()
    return {"tracked": True}


@router.get("/dashboard")
async def dashboard(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """User's personal dashboard analytics"""
    # User's content counts
    startups = await db.scalar(select(func.count(Startup.id)).where(Startup.owner_id == user.id)) or 0
    jobs = await db.scalar(select(func.count(Job.id)).where(Job.company_id == user.id)) or 0
    services = await db.scalar(select(func.count(FreelancerService.id)).where(FreelancerService.user_id == user.id)) or 0
    ai_requests = await db.scalar(select(func.count(AIRequest.id)).where(AIRequest.user_id == user.id)) or 0
    ai_tokens = await db.scalar(select(func.sum(AIRequest.tokens_used)).where(AIRequest.user_id == user.id)) or 0
    
    # Last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_ai = await db.scalar(select(func.count(AIRequest.id)).where(AIRequest.user_id == user.id, AIRequest.created_at >= week_ago)) or 0
    
    return {
        "startups": startups, "jobs": jobs, "services": services,
        "ai_requests_total": ai_requests, "ai_tokens_used": ai_tokens,
        "ai_requests_week": recent_ai, "tokens_balance": user.tokens,
        "is_premium": user.is_premium, "premium_expires": user.premium_expires.isoformat() if user.premium_expires else None
    }


@router.get("/admin/overview")
async def admin_overview(user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    """Admin global analytics"""
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    return {
        "users": {
            "total": await db.scalar(select(func.count(User.id))) or 0,
            "today": await db.scalar(select(func.count(User.id)).where(User.created_at >= today)) or 0,
            "week": await db.scalar(select(func.count(User.id)).where(User.created_at >= week_ago)) or 0,
            "month": await db.scalar(select(func.count(User.id)).where(User.created_at >= month_ago)) or 0,
            "premium": await db.scalar(select(func.count(User.id)).where(User.is_premium == True)) or 0,
        },
        "content": {
            "startups": await db.scalar(select(func.count(Startup.id))) or 0,
            "jobs": await db.scalar(select(func.count(Job.id))) or 0,
            "services": await db.scalar(select(func.count(FreelancerService.id))) or 0,
        },
        "ai": {
            "total": await db.scalar(select(func.count(AIRequest.id))) or 0,
            "today": await db.scalar(select(func.count(AIRequest.id)).where(AIRequest.created_at >= today)) or 0,
            "tokens": await db.scalar(select(func.sum(AIRequest.tokens_used))) or 0,
        }
    }


@router.get("/admin/events")
async def admin_events(days: int = 7, user: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    """Top events"""
    since = datetime.utcnow() - timedelta(days=days)
    r = await db.execute(
        select(Analytics.event, func.count(Analytics.id))
        .where(Analytics.created_at >= since).group_by(Analytics.event)
        .order_by(func.count(Analytics.id).desc()).limit(20)
    )
    return [{"event": e, "count": c} for e, c in r.all()]
