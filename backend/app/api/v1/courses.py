"""Courses API - learning platform"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Course, Lesson, Enrollment, CourseLevel

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    level: str = "beginner"
    price: float = 0
    cover_image: Optional[str] = None
    tags: List[str] = []
    lessons: List[dict] = []  # [{title, content, video_url, duration}]


class LessonCreate(BaseModel):
    title: str
    content: str
    video_url: Optional[str] = None
    duration: int = 0  # minutes
    order: int = 0


@router.get("/")
async def list_courses(search: Optional[str] = None, category: Optional[str] = None, level: Optional[str] = None, limit: int = Query(50, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Course).where(Course.is_published == True)
    if search: q = q.where(Course.title.ilike(f"%{search}%"))
    if category: q = q.where(Course.category == category)
    if level: q = q.where(Course.level == level)
    q = q.order_by(Course.is_featured.desc(), Course.students_count.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": c.id, "title": c.title, "description": c.description, "category": c.category, "level": c.level.value, "price": c.price, "cover_image": c.cover_image, "tags": c.tags, "students_count": c.students_count, "rating": c.rating, "lessons_count": c.lessons_count, "duration_hours": c.duration_hours, "instructor": c.instructor_name, "is_featured": c.is_featured, "created_at": c.created_at.isoformat()} for c in r.scalars().all()]


@router.get("/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    c = await db.get(Course, course_id)
    if not c: raise HTTPException(404)
    r = await db.execute(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order))
    lessons = [{"id": l.id, "title": l.title, "video_url": l.video_url, "duration": l.duration, "order": l.order} for l in r.scalars().all()]
    return {"id": c.id, "title": c.title, "description": c.description, "category": c.category, "level": c.level.value, "price": c.price, "cover_image": c.cover_image, "tags": c.tags, "students_count": c.students_count, "rating": c.rating, "lessons_count": c.lessons_count, "duration_hours": c.duration_hours, "instructor": c.instructor_name, "lessons": lessons}


@router.post("/")
async def create_course(req: CourseCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = Course(instructor_id=user.id, instructor_name=user.full_name, title=req.title, description=req.description, category=req.category, level=CourseLevel(req.level), price=req.price, cover_image=req.cover_image, tags=req.tags, lessons_count=len(req.lessons))
    db.add(c)
    await db.flush()
    for i, l in enumerate(req.lessons):
        lesson = Lesson(course_id=c.id, title=l.get("title", ""), content=l.get("content", ""), video_url=l.get("video_url"), duration=l.get("duration", 0), order=l.get("order", i))
        db.add(lesson)
    c.duration_hours = sum(l.get("duration", 0) for l in req.lessons) / 60
    await db.commit()
    return {"id": c.id}


@router.post("/{course_id}/enroll")
async def enroll(course_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Course, course_id)
    if not c: raise HTTPException(404)
    existing = await db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if existing: return {"message": "Siz allaqachon yozilgansiz"}
    db.add(Enrollment(user_id=user.id, course_id=course_id))
    c.students_count += 1
    await db.commit()
    return {"message": "Yozildingiz"}


@router.post("/{course_id}/lessons/{lesson_id}/complete")
async def complete_lesson(course_id: int, lesson_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    e = await db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if not e: raise HTTPException(403, "Avval yoziling")
    e.completed_lessons = list(set((e.completed_lessons or []) + [lesson_id]))
    e.progress = len(e.completed_lessons)
    await db.commit()
    return {"progress": e.progress}


@router.get("/my/enrolled")
async def my_courses(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Course, Enrollment).join(Enrollment, Enrollment.course_id == Course.id)
        .where(Enrollment.user_id == user.id)
    )
    return [{"id": c.id, "title": c.title, "cover_image": c.cover_image, "progress": e.progress, "enrolled_at": e.enrolled_at.isoformat()} for c, e in r.all()]
