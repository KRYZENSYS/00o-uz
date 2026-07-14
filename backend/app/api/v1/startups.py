"""Startups API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel
from typing import Optional
import re

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Startup, StartupCategory, StartupStage, Like

router = APIRouter(prefix="/startups", tags=["startups"])


class StartupCreate(BaseModel):
    name: str
    tagline: str
    description: str
    category: str
    stage: str
    website: Optional[str] = None
    location: Optional[str] = None
    funding_goal: float = 0
    logo: Optional[str] = None


def slugify(t: str) -> str:
    t = re.sub(r'[^\w\s-]', '', t.lower())
    return re.sub(r'[-\s]+', '-', t).strip('-')


@router.get("/")
async def list_startups(search: Optional[str] = None, category: Optional[str] = None, stage: Optional[str] = None, limit: int = Query(50, le=100), offset: int = 0, db: AsyncSession = Depends(get_db)):
    q = select(Startup).where(Startup.is_active == True)
    if search: q = q.where(or_(Startup.name.ilike(f"%{search}%"), Startup.tagline.ilike(f"%{search}%")))
    if category: q = q.where(Startup.category == category)
    if stage: q = q.where(Startup.stage == stage)
    q = q.order_by(Startup.is_featured.desc(), Startup.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(q)
    return [{"id": s.id, "name": s.name, "slug": s.slug, "tagline": s.tagline, "logo": s.logo,
             "category": s.category.value, "stage": s.stage.value, "location": s.location,
             "views_count": s.views_count, "likes_count": s.likes_count, "is_verified": s.is_verified,
             "is_featured": s.is_featured, "funding_raised": s.funding_raised} for s in result.scalars().all()]


@router.get("/trending/list")
async def trending(limit: int = 10, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Startup).where(Startup.is_active == True).order_by(Startup.views_count.desc()).limit(limit))
    return [{"id": s.id, "name": s.name, "tagline": s.tagline, "views_count": s.views_count} for s in r.scalars().all()]


@router.get("/{sid}")
async def get_startup(sid: int, db: AsyncSession = Depends(get_db)):
    s = await db.get(Startup, sid)
    if not s or not s.is_active: raise HTTPException(404, "Not found")
    s.views_count += 1; await db.commit()
    return {"id": s.id, "name": s.name, "slug": s.slug, "tagline": s.tagline, "description": s.description,
            "logo": s.logo, "category": s.category.value, "stage": s.stage.value, "location": s.location,
            "views_count": s.views_count, "likes_count": s.likes_count, "is_verified": s.is_verified,
            "is_featured": s.is_featured, "funding_raised": s.funding_raised}


@router.post("/")
async def create(req, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = Startup(owner_id=user.id, name=req.name, slug=slugify(req.name), tagline=req.tagline,
                description=req.description, category=StartupCategory(req.category), stage=StartupStage(req.stage),
                website=req.website, location=req.location, funding_goal=req.funding_goal, logo=req.logo)
    db.add(s); await db.commit()
    return {"id": s.id, "slug": s.slug}


@router.post("/{sid}/like")
async def like(sid: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Like).where(Like.user_id == user.id, Like.target_type == "startup", Like.target_id == sid))
    s = await db.get(Startup, sid)
    if existing.scalar_one_or_none():
        await db.execute(Like.__table__.delete().where(Like.user_id == user.id, Like.target_type == "startup", Like.target_id == sid))
        if s: s.likes_count = max(0, s.likes_count - 1)
        await db.commit()
        return {"liked": False, "count": s.likes_count if s else 0}
    db.add(Like(user_id=user.id, target_type="startup", target_id=sid))
    if s: s.likes_count += 1
    await db.commit()
    return {"liked": True, "count": s.likes_count if s else 0}
