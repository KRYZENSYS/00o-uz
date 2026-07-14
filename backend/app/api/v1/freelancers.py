"""Freelancer Services & Jobs API"""
from typing import Optional, List
import re, secrets
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, FreelancerService, Job

router = APIRouter()


class ServiceCreate(BaseModel):
    title: str
    description: str
    category: str = "other"
    subcategory: Optional[str] = None
    basic_price: float = 0
    standard_price: float = 0
    premium_price: float = 0
    basic_delivery_days: int = 7
    standard_delivery_days: int = 14
    premium_delivery_days: int = 30
    cover_image: Optional[str] = None
    gallery: List[str] = []
    tags: List[str] = []


@router.get("/services", tags=["freelancers"])
async def list_services(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(FreelancerService).where(FreelancerService.is_active == True)
    if category: query = query.where(FreelancerService.category == category)
    if search:
        query = query.where(or_(
            FreelancerService.title.ilike(f"%{search}%"),
            FreelancerService.description.ilike(f"%{search}%"),
        ))
    if min_price: query = query.where(FreelancerService.basic_price >= min_price)
    if max_price: query = query.where(FreelancerService.basic_price <= max_price)
    query = query.order_by(FreelancerService.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    items = result.scalars().all()
    return [{
        "id": s.id, "title": s.title, "slug": s.slug, "description": s.description,
        "category": s.category.value, "cover_image": s.cover_image,
        "basic_price": s.basic_price, "standard_price": s.standard_price,
        "premium_price": s.premium_price, "rating": s.rating,
        "reviews_count": s.reviews_count, "orders_count": s.orders_count,
        "freelancer_id": s.freelancer_id, "tags": s.tags
    } for s in items]


@router.post("/services", tags=["freelancers"], status_code=201)
async def create_service(data: ServiceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    slug = re.sub(r'[^a-z0-9]+', '-', data.title.lower()).strip('-')
    existing = await db.execute(select(FreelancerService).where(FreelancerService.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-{secrets.token_hex(3)}"
    service = FreelancerService(
        freelancer_id=current_user.id, title=data.title, slug=slug, description=data.description,
        category=data.category, subcategory=data.subcategory, basic_price=data.basic_price,
        standard_price=data.standard_price, premium_price=data.premium_price,
        basic_delivery_days=data.basic_delivery_days, standard_delivery_days=data.standard_delivery_days,
        premium_delivery_days=data.premium_delivery_days, cover_image=data.cover_image,
        gallery=data.gallery, tags=data.tags,
    )
    db.add(service); await db.commit(); await db.refresh(service)
    return {"id": service.id, "title": service.title, "slug": service.slug}


class JobCreate(BaseModel):
    title: str
    description: str
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    category: Optional[str] = None
    job_type: str = "full_time"
    work_mode: str = "remote"
    location: Optional[str] = None
    salary_min: float = 0
    salary_max: float = 0
    salary_currency: str = "UZS"
    experience_years: int = 0
    skills: List[str] = []


@router.get("/jobs", tags=["jobs"])
async def list_jobs(
    job_type: Optional[str] = None,
    work_mode: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(Job).where(Job.is_active == True)
    if job_type: query = query.where(Job.job_type == job_type)
    if work_mode: query = query.where(Job.work_mode == work_mode)
    if search:
        query = query.where(or_(Job.title.ilike(f"%{search}%"), Job.description.ilike(f"%{search}%")))
    query = query.order_by(Job.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    items = result.scalars().all()
    return [{
        "id": j.id, "title": j.title, "slug": j.slug, "description": j.description,
        "company_name": j.company_name, "company_logo": j.company_logo,
        "job_type": j.job_type.value, "work_mode": j.work_mode.value,
        "location": j.location, "salary_min": j.salary_min, "salary_max": j.salary_max,
        "salary_currency": j.salary_currency, "skills": j.skills,
        "applicants_count": j.applicants_count, "created_at": j.created_at.isoformat()
    } for j in items]


@router.post("/jobs", tags=["jobs"], status_code=201)
async def create_job(data: JobCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    slug = re.sub(r'[^a-z0-9]+', '-', data.title.lower()).strip('-')
    existing = await db.execute(select(Job).where(Job.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-{secrets.token_hex(3)}"
    job = Job(
        employer_id=current_user.id, title=data.title, slug=slug, description=data.description,
        company_name=data.company_name, company_logo=data.company_logo, category=data.category,
        job_type=data.job_type, work_mode=data.work_mode, location=data.location,
        salary_min=data.salary_min, salary_max=data.salary_max,
        salary_currency=data.salary_currency, experience_years=data.experience_years, skills=data.skills,
    )
    db.add(job); await db.commit(); await db.refresh(job)
    return {"id": job.id, "title": job.title, "slug": job.slug}
