"""Education Platform - Live classes, courses, certificates, homework"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Course, Lesson, Enrollment, LessonProgress, LiveClass, ClassAttendee, Homework, HomeworkSubmission, Certificate, Discussion, DiscussionReply

router = APIRouter(prefix="/education", tags=["education"])


class CourseCreateReq(BaseModel):
    title: str
    description: str
    category: str
    level: str = "beginner"
    price: float = 0
    cover_image: Optional[str] = None
    requirements: Optional[List[str]] = []
    what_you_learn: Optional[List[str]] = []


class LessonReq(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration_minutes: int
    materials: Optional[List[str]] = []
    order: int = 0


class LiveClassReq(BaseModel):
    course_id: Optional[int] = None
    title: str
    description: str
    scheduled_at: datetime
    duration_minutes: int = 60
    max_attendees: int = 100


class HomeworkReq(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    title: str
    description: str
    due_date: datetime
    max_score: int = 100


class HomeworkSubmitReq(BaseModel):
    homework_id: int
    text: Optional[str] = None
    files: Optional[List[str]] = []


# ============ COURSES ============
@router.post("/courses")
async def create_course(req: CourseCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = Course(instructor_id=user.id, **req.dict(), is_published=False)
    db.add(c); await db.commit(); await db.refresh(c)
    return {"id": c.id}


@router.get("/courses")
async def list_courses(category: Optional[str] = None, level: Optional[str] = None, search: Optional[str] = None, sort: str = "newest", limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(Course).where(Course.is_published == True)
    if category: q = q.where(Course.category == category)
    if level: q = q.where(Course.level == level)
    if search: q = q.where(Course.title.ilike(f"%{search}%"))
    if sort == "popular": q = q.order_by(Course.students_count.desc())
    elif sort == "rating": q = q.order_by(Course.rating.desc())
    else: q = q.order_by(Course.created_at.desc())
    q = q.limit(limit)
    r = await db.execute(q)
    return [{"id": c.id, "title": c.title, "description": c.description, "category": c.category, "level": c.level, "price": c.price, "cover_image": c.cover_image, "instructor": c.instructor.full_name if c.instructor else None, "rating": c.rating, "students_count": c.students_count, "lessons_count": c.lessons_count, "duration_hours": c.duration_hours} for c in r.scalars().all()]


@router.get("/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    c = await db.get(Course, course_id)
    if not c: raise HTTPException(404)
    c.views_count += 1
    await db.commit()
    return {"id": c.id, "title": c.title, "description": c.description, "category": c.category, "level": c.level, "price": c.price, "cover_image": c.cover_image, "requirements": c.requirements, "what_you_learn": c.what_you_learn, "rating": c.rating, "students_count": c.students_count, "lessons_count": c.lessons_count, "instructor": {"id": c.instructor.id, "full_name": c.instructor.full_name, "avatar_url": c.instructor.avatar_url}}


@router.post("/courses/{course_id}/enroll")
async def enroll(course_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Course, course_id)
    if not c: raise HTTPException(404)
    existing = await db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if existing: return {"message": "Allaqachon yozilgan"}
    db.add(Enrollment(user_id=user.id, course_id=course_id, progress=0))
    c.students_count += 1
    await db.commit()
    return {"message": "Yozildingiz"}


# ============ LESSONS ============
@router.post("/courses/{course_id}/lessons")
async def add_lesson(course_id: int, req: LessonReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Course, course_id)
    if not c or c.instructor_id != user.id: raise HTTPException(403)
    l = Lesson(course_id=course_id, **req.dict())
    db.add(l); await db.commit()
    c.lessons_count = (c.lessons_count or 0) + 1
    c.duration_hours = (c.duration_hours or 0) + l.duration_minutes / 60
    await db.commit()
    return {"id": l.id}


@router.get("/courses/{course_id}/lessons")
async def list_lessons(course_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order))
    return [{"id": l.id, "title": l.title, "duration_minutes": l.duration_minutes, "video_url": l.video_url, "order": l.order, "is_free": l.is_free} for l in r.scalars().all()]


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    l = await db.get(Lesson, lesson_id)
    if not l: raise HTTPException(404)
    existing = await db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id))
    if not existing: db.add(LessonProgress(user_id=user.id, lesson_id=lesson_id, course_id=l.course_id, completed_at=datetime.utcnow()))
    await db.commit()
    
    # Update course progress
    total = await db.scalar(select(func.count(Lesson.id)).where(Lesson.course_id == l.course_id)) or 1
    completed = await db.scalar(select(func.count(LessonProgress.id)).where(LessonProgress.user_id == user.id, LessonProgress.course_id == l.course_id)) or 0
    progress = (completed / total) * 100
    enr = await db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == l.course_id))
    if enr: enr.progress = progress
    await db.commit()
    return {"progress": progress, "completed_lessons": completed, "total_lessons": total}


# ============ LIVE CLASSES ============
@router.post("/live-classes")
async def schedule_class(req: LiveClassReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lc = LiveClass(instructor_id=user.id, **req.dict(), status="scheduled", join_url=f"https://00o.uz/class/{secrets_token()}")
    db.add(lc); await db.commit(); await db.refresh(lc)
    return {"id": lc.id, "join_url": lc.join_url}


@router.get("/live-classes/upcoming")
async def upcoming_classes(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(LiveClass).where(LiveClass.scheduled_at > datetime.utcnow(), LiveClass.status == "scheduled").order_by(LiveClass.scheduled_at).limit(20))
    return [{"id": lc.id, "title": lc.title, "scheduled_at": lc.scheduled_at.isoformat(), "instructor": lc.instructor.full_name if lc.instructor else None, "attendees": lc.attendees_count} for lc in r.scalars().all()]


@router.post("/live-classes/{class_id}/join")
async def join_class(class_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lc = await db.get(LiveClass, class_id)
    if not lc: raise HTTPException(404)
    existing = await db.scalar(select(ClassAttendee).where(ClassAttendee.class_id == class_id, ClassAttendee.user_id == user.id))
    if not existing: db.add(ClassAttendee(class_id=class_id, user_id=user.id)); lc.attendees_count += 1; await db.commit()
    return {"join_url": lc.join_url}


# ============ HOMEWORK ============
@router.post("/homework")
async def create_homework(req: HomeworkReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    hw = Homework(creator_id=user.id, **req.dict())
    db.add(hw); await db.commit(); await db.refresh(hw)
    return {"id": hw.id}


@router.post("/homework/submit")
async def submit_homework(req: HomeworkSubmitReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = HomeworkSubmission(user_id=user.id, **req.dict(), submitted_at=datetime.utcnow(), status="submitted")
    db.add(s); await db.commit()
    return {"id": s.id, "status": "submitted"}


@router.post("/homework/{submission_id}/grade")
async def grade_homework(submission_id: int, score: int, feedback: str = "", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(HomeworkSubmission, submission_id)
    if not s: raise HTTPException(404)
    s.score = score; s.feedback = feedback; s.status = "graded"; s.graded_at = datetime.utcnow()
    await db.commit()
    return {"score": score}


# ============ CERTIFICATES ============
@router.post("/courses/{course_id}/certificate")
async def issue_certificate(course_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    enr = await db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if not enr: raise HTTPException(404, "Avval yoziling")
    if enr.progress < 100: raise HTTPException(400, f"Kurs tugamagan. Progress: {enr.progress}%")
    
    cert = Certificate(user_id=user.id, course_id=course_id, code=f"CERT-{secrets_token()[:12].upper()}", issued_at=datetime.utcnow(), pdf_url=f"/certificates/{user.id}_{course_id}.pdf")
    db.add(cert); await db.commit()
    return {"id": cert.id, "code": cert.code, "pdf_url": cert.pdf_url}


@router.get("/certificates/my")
async def my_certificates(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Certificate, Course).join(Course, Course.id == Certificate.course_id).where(Certificate.user_id == user.id))
    return [{"id": c.id, "course": cr.title, "code": c.code, "issued_at": c.issued_at.isoformat(), "pdf_url": c.pdf_url} for c, cr in r.all()]


# ============ DISCUSSIONS ============
@router.post("/discussions")
async def create_discussion(course_id: int, title: str, content: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = Discussion(course_id=course_id, user_id=user.id, title=title, content=content)
    db.add(d); await db.commit(); await db.refresh(d)
    return {"id": d.id}


@router.get("/discussions/{course_id}")
async def list_discussions(course_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Discussion).where(Discussion.course_id == course_id).order_by(Discussion.created_at.desc()))
    return [{"id": d.id, "title": d.title, "content": d.content, "replies_count": d.replies_count, "user": d.user.full_name, "created_at": d.created_at.isoformat()} for d in r.scalars().all()]


@router.post("/discussions/{discussion_id}/reply")
async def reply_discussion(discussion_id: int, content: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = DiscussionReply(discussion_id=discussion_id, user_id=user.id, content=content)
    db.add(r)
    d = await db.get(Discussion, discussion_id)
    if d: d.replies_count = (d.replies_count or 0) + 1
    await db.commit()
    return {"id": r.id}


def secrets_token(n=16):
    import secrets
    return secrets.token_urlsafe(n)
