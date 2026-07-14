"""Global Search API - search across all content"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import Optional

from app.core.database import get_db
from app.models import User, Startup, Job, FreelancerService, Course, Investor

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def global_search(
    q: str = Query(min_length=2),
    type: Optional[str] = None,  # all, startups, jobs, services, users, courses, investors
    limit: int = Query(20, le=50),
    db: AsyncSession = Depends(get_db)
):
    results = {"query": q, "users": [], "startups": [], "jobs": [], "services": [], "courses": [], "investors": [], "total": 0}
    
    if not type or type == "all" or type == "users":
        r = await db.execute(
            select(User).where(or_(User.username.ilike(f"%{q}%"), User.full_name.ilike(f"%{q}%")))
            .where(User.is_active == True).limit(limit)
        )
        results["users"] = [{"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "bio": u.bio, "is_premium": u.is_premium} for u in r.scalars().all()]
    
    if not type or type == "all" or type == "startups":
        r = await db.execute(
            select(Startup).where(or_(Startup.name.ilike(f"%{q}%"), Startup.tagline.ilike(f"%{q}%"), Startup.description.ilike(f"%{q}%")))
            .where(Startup.is_active == True).order_by(Startup.views_count.desc()).limit(limit)
        )
        results["startups"] = [{"id": s.id, "name": s.name, "slug": s.slug, "tagline": s.tagline, "logo": s.logo, "category": s.category.value, "stage": s.stage.value, "views_count": s.views_count, "likes_count": s.likes_count} for s in r.scalars().all()]
    
    if not type or type == "all" or type == "jobs":
        r = await db.execute(
            select(Job).where(or_(Job.title.ilike(f"%{q}%"), Job.description.ilike(f"%{q}%")))
            .where(Job.is_active == True).order_by(Job.created_at.desc()).limit(limit)
        )
        results["jobs"] = [{"id": j.id, "title": j.title, "category": j.category, "job_type": j.job_type.value, "location": j.location, "is_remote": j.is_remote, "salary_min": j.salary_min, "salary_max": j.salary_max, "created_at": j.created_at.isoformat()} for j in r.scalars().all()]
    
    if not type or type == "all" or type == "services":
        r = await db.execute(
            select(FreelancerService).where(or_(FreelancerService.title.ilike(f"%{q}%"), FreelancerService.description.ilike(f"%{q}%")))
            .where(FreelancerService.is_active == True).order_by(FreelancerService.rating.desc()).limit(limit)
        )
        results["services"] = [{"id": s.id, "title": s.title, "category": s.category, "price_basic": s.price_basic, "rating": s.rating, "orders_count": s.orders_count, "delivery_days": s.delivery_days} for s in r.scalars().all()]
    
    if not type or type == "all" or type == "courses":
        r = await db.execute(
            select(Course).where(or_(Course.title.ilike(f"%{q}%"), Course.description.ilike(f"%{q}%")))
            .where(Course.is_published == True).order_by(Course.students_count.desc()).limit(limit)
        )
        results["courses"] = [{"id": c.id, "title": c.title, "category": c.category, "level": c.level.value, "price": c.price, "students_count": c.students_count, "rating": c.rating, "cover_image": c.cover_image} for c in r.scalars().all()]
    
    if not type or type == "all" or type == "investors":
        r = await db.execute(
            select(Investor).where(or_(Investor.name.ilike(f"%{q}%"), Investor.bio.ilike(f"%{q}%")))
            .where(Investor.is_active == True).limit(limit)
        )
        results["investors"] = [{"id": i.id, "name": i.name, "type": i.type.value, "bio": i.bio, "min_investment": i.min_investment, "max_investment": i.max_investment, "is_verified": i.is_verified} for i in r.scalars().all()]
    
    results["total"] = sum(len(results[k]) for k in ["users", "startups", "jobs", "services", "courses", "investors"])
    return results


@router.get("/suggestions")
async def suggestions(q: str = Query(min_length=1), db: AsyncSession = Depends(get_db)):
    """Quick search suggestions"""
    suggestions = []
    r = await db.execute(select(Startup.name).where(Startup.name.ilike(f"%{q}%")).where(Startup.is_active == True).limit(5))
    for (n,) in r.all(): suggestions.append({"text": n, "type": "startup"})
    
    r = await db.execute(select(Job.title).where(Job.title.ilike(f"%{q}%")).where(Job.is_active == True).limit(5))
    for (t,) in r.all(): suggestions.append({"text": t, "type": "job"})
    
    return suggestions[:10]
