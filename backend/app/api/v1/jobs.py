"""Jobs API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Job, JobType

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobCreate(BaseModel):
    title: str
    description: str
    category: str
    job_type: str
    location: Optional[str] = None
    is_remote: bool = False
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    skills: List[str] = []


@router.get("/")
async def list_jobs(search: Optional[str] = None, category: Optional[str] = None, job_type: Optional[str] = None, is_remote: Optional[bool] = None, limit: int = Query(50, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Job).where(Job.is_active == True)
    if search: q = q.where(or_(Job.title.ilike(f"%{search}%"), Job.description.ilike(f"%{search}%")))
    if category: q = q.where(Job.category == category)
    if job_type: q = q.where(Job.job_type == job_type)
    if is_remote is not None: q = q.where(Job.is_remote == is_remote)
    q = q.order_by(Job.is_featured.desc(), Job.created_at.desc()).limit(limit)
    result = await db.execute(q)
    return [{"id": j.id, "title": j.title, "category": j.category, "job_type": j.job_type.value,
             "location": j.location, "is_remote": j.is_remote, "salary_min": j.salary_min,
             "salary_max": j.salary_max, "currency": j.currency, "skills": j.skills,
             "is_featured": j.is_featured, "created_at": j.created_at.isoformat()} for j in result.scalars().all()]


@router.get("/{jid}")
async def get_job(jid: int, db: AsyncSession = Depends(get_db)):
    j = await db.get(Job, jid)
    if not j: raise HTTPException(404)
    return {"id": j.id, "title": j.title, "description": j.description, "category": j.category,
            "job_type": j.job_type.value, "location": j.location, "is_remote": j.is_remote,
            "salary_min": j.salary_min, "salary_max": j.salary_max, "skills": j.skills}


@router.post("/")
async def create(req: JobCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    j = Job(company_id=user.id, title=req.title, description=req.description, category=req.category,
            job_type=JobType(req.job_type), location=req.location, is_remote=req.is_remote,
            salary_min=req.salary_min, salary_max=req.salary_max, skills=req.skills)
    db.add(j); await db.commit()
    return {"id": j.id}


@router.post("/{jid}/apply")
async def apply(jid: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    j = await db.get(Job, jid)
    if not j: raise HTTPException(404)
    j.applicants_count += 1; await db.commit()
    return {"message": "Arizangiz qabul qilindi"}
