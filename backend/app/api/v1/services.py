"""Services API"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, FreelancerService

router = APIRouter(prefix="/services", tags=["services"])


class ServiceCreate(BaseModel):
    title: str
    description: str
    category: str
    price_basic: float
    price_standard: Optional[float] = None
    price_premium: Optional[float] = None
    delivery_days: int = 7
    tags: List[str] = []


@router.get("/")
async def list_services(search: Optional[str] = None, category: Optional[str] = None, limit: int = Query(50, le=100), db: AsyncSession = Depends(get_db)):
    q = select(FreelancerService).where(FreelancerService.is_active == True)
    if search: q = q.where(or_(FreelancerService.title.ilike(f"%{search}%"), FreelancerService.description.ilike(f"%{search}%")))
    if category: q = q.where(FreelancerService.category == category)
    q = q.order_by(FreelancerService.is_featured.desc(), FreelancerService.rating.desc()).limit(limit)
    result = await db.execute(q)
    return [{"id": s.id, "user_id": s.user_id, "title": s.title, "description": s.description,
             "category": s.category, "price_basic": s.price_basic, "price_standard": s.price_standard,
             "price_premium": s.price_premium, "delivery_days": s.delivery_days, "tags": s.tags,
             "rating": s.rating, "orders_count": s.orders_count, "is_featured": s.is_featured}
            for s in result.scalars().all()]


@router.post("/")
async def create(req: ServiceCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = FreelancerService(user_id=user.id, title=req.title, description=req.description, category=req.category,
                          price_basic=req.price_basic, price_standard=req.price_standard, price_premium=req.price_premium,
                          delivery_days=req.delivery_days, tags=req.tags)
    db.add(s); await db.commit()
    return {"id": s.id}
