"""Startups API: CRUD, search, filter"""
from typing import Optional, List
import re, secrets
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Startup

router = APIRouter(prefix="/startups", tags=["startups"])


class StartupCreate(BaseModel):
    name: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    category: str = "other"
    stage: str = "idea"
    funding_goal: float = 0
    logo: Optional[str] = None
    banner: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None
    team_size: int = 1
    tags: List[str] = []


@router.get("")
async def list_startups(
    category: Optional[str] = None,
    stage: Optional[str] = None,
    search: Optional[str] = None,
    featured: Optional[bool] = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(Startup).where(Startup.is_active == True)
    if category: query = query.where(Startup.category == category)
    if stage: query = query.where(Startup.stage == stage)
    if search:
        query = query.where(or_(
            Startup.name.ilike(f"%{search}%"),
            Startup.tagline.ilike(f"%{search}%"),
        ))
    if featured: query = query.where(Startup.is_featured == True)
    query = query.order_by(Startup.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    items = result.scalars().all()
    return [{
        "id": s.id, "name": s.name, "slug": s.slug, "tagline": s.tagline,
        "description": s.description, "category": s.category.value, "stage": s.stage.value,
        "logo": s.logo, "banner": s.banner, "funding_goal": s.funding_goal,
        "funding_raised": s.funding_raised, "team_size": s.team_size,
        "location": s.location, "is_verified": s.is_verified, "is_featured": s.is_featured,
        "views_count": s.views_count, "likes_count": s.likes_count,
        "created_at": s.created_at.isoformat()
    } for s in items]


@router.post("", status_code=201)
async def create_startup(data: StartupCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    slug = re.sub(r'[^a-z0-9]+', '-', data.name.lower()).strip('-')
    existing = await db.execute(select(Startup).where(Startup.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-{secrets.token_hex(3)}"
    startup = Startup(
        owner_id=current_user.id, name=data.name, slug=slug,
        tagline=data.tagline, description=data.description,
        category=data.category, stage=data.stage, funding_goal=data.funding_goal,
        logo=data.logo, banner=data.banner, website=data.website, github=data.github,
        location=data.location, team_size=data.team_size, tags=data.tags,
    )
    db.add(startup); await db.commit(); await db.refresh(startup)
    return {"id": startup.id, "name": startup.name, "slug": startup.slug, "message": "Created"}


@router.get("/{startup_id}")
async def get_startup(startup_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    s = result.scalar_one_or_none()
    if not s: raise HTTPException(status_code=404, detail="Not found")
    s.views_count += 1
    await db.commit()
    return {
        "id": s.id, "name": s.name, "slug": s.slug, "tagline": s.tagline,
        "description": s.description, "category": s.category.value, "stage": s.stage.value,
        "logo": s.logo, "banner": s.banner, "funding_goal": s.funding_goal,
        "funding_raised": s.funding_raised, "team_size": s.team_size,
        "location": s.location, "is_verified": s.is_verified, "is_featured": s.is_featured,
        "views_count": s.views_count, "likes_count": s.likes_count,
        "owner_id": s.owner_id, "website": s.website, "github": s.github,
        "created_at": s.created_at.isoformat()
    }


@router.post("/{startup_id}/like")
async def like_startup(startup_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    s = result.scalar_one_or_none()
    if not s: raise HTTPException(status_code=404, detail="Not found")
    s.likes_count += 1
    await db.commit()
    return {"likes": s.likes_count}


@router.get("/trending/list")
async def trending(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Startup).where(Startup.is_active == True)
        .order_by((Startup.likes_count + Startup.views_count).desc()).limit(limit)
    )
    items = result.scalars().all()
    return [{"id": s.id, "name": s.name, "tagline": s.tagline, "logo": s.logo,
             "category": s.category.value, "funding_raised": s.funding_raised} for s in items]
