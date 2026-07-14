"""Events, Communities, Polls, Quizzes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Event, EventAttendee, Community, CommunityMember, Poll, PollOption, PollVote, Quiz, QuizQuestion, QuizAttempt

router = APIRouter(prefix="/social", tags=["social"])


# ============ EVENTS ============
class EventCreateReq(BaseModel):
    title: str
    description: str
    category: str
    start_at: datetime
    end_at: datetime
    location: Optional[str] = None
    is_online: bool = True
    online_url: Optional[str] = None
    cover_image: Optional[str] = None
    max_attendees: Optional[int] = None
    is_free: bool = True
    price: float = 0


@router.post("/events")
async def create_event(req: EventCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    e = Event(**req.dict(), organizer_id=user.id)
    db.add(e); await db.commit(); await db.refresh(e)
    return {"id": e.id, "title": e.title}


@router.get("/events")
async def list_events(category: Optional[str] = None, upcoming_only: bool = True, limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(Event).where(Event.is_cancelled == False)
    if category: q = q.where(Event.category == category)
    if upcoming_only: q = q.where(Event.start_at > datetime.utcnow())
    q = q.order_by(Event.start_at).limit(limit)
    r = await db.execute(q)
    return [{"id": e.id, "title": e.title, "description": e.description, "category": e.category, "start_at": e.start_at.isoformat(), "location": e.location, "is_online": e.is_online, "attendees_count": e.attendees_count, "cover_image": e.cover_image, "is_free": e.is_free, "price": e.price} for e in r.scalars().all()]


@router.post("/events/{event_id}/rsvp")
async def rsvp(event_id: int, status: str = "going", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    e = await db.get(Event, event_id)
    if not e: raise HTTPException(404)
    existing = await db.scalar(select(EventAttendee).where(EventAttendee.event_id == event_id, EventAttendee.user_id == user.id))
    if existing: existing.status = status
    else:
        db.add(EventAttendee(event_id=event_id, user_id=user.id, status=status))
        e.attendees_count += 1
    await db.commit()
    return {"status": status, "attendees": e.attendees_count}


# ============ COMMUNITIES ============
class CommunityCreateReq(BaseModel):
    name: str
    description: str
    category: str
    cover_image: Optional[str] = None
    is_private: bool = False
    rules: Optional[str] = None


@router.post("/communities")
async def create_community(req: CommunityCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = Community(**req.dict(), owner_id=user.id, members_count=1)
    db.add(c); await db.commit(); await db.refresh(c)
    db.add(CommunityMember(community_id=c.id, user_id=user.id, role="owner"))
    await db.commit()
    return {"id": c.id, "name": c.name}


@router.get("/communities")
async def list_communities(category: Optional[str] = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(Community).where(Community.is_private == False)
    if category: q = q.where(Community.category == category)
    q = q.order_by(Community.members_count.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": c.id, "name": c.name, "description": c.description, "category": c.category, "cover_image": c.cover_image, "members_count": c.members_count, "posts_count": c.posts_count} for c in r.scalars().all()]


@router.post("/communities/{community_id}/join")
async def join_community(community_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Community, community_id)
    if not c: raise HTTPException(404)
    existing = await db.scalar(select(CommunityMember).where(CommunityMember.community_id == community_id, CommunityMember.user_id == user.id))
    if not existing:
        db.add(CommunityMember(community_id=community_id, user_id=user.id, role="member"))
        c.members_count += 1
        await db.commit()
    return {"members": c.members_count}


@router.post("/communities/{community_id}/leave")
async def leave_community(community_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Community, community_id)
    if not c: raise HTTPException(404)
    m = await db.scalar(select(CommunityMember).where(CommunityMember.community_id == community_id, CommunityMember.user_id == user.id))
    if m:
        await db.delete(m)
        c.members_count = max(0, c.members_count - 1)
        await db.commit()
    return {"members": c.members_count}


# ============ POLLS ============
class PollCreateReq(BaseModel):
    question: str
    options: List[str]
    is_multiple: bool = False
    expires_at: Optional[datetime] = None


@router.post("/polls")
async def create_poll(req: PollCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = Poll(user_id=user.id, question=req.question, is_multiple=req.is_multiple, expires_at=req.expires_at)
    db.add(p); await db.commit(); await db.refresh(p)
    for opt in req.options:
        db.add(PollOption(poll_id=p.id, text=opt))
    await db.commit()
    return {"id": p.id, "question": p.question, "options_count": len(req.options)}


@router.get("/polls/{poll_id}")
async def get_poll(poll_id: int, db: AsyncSession = Depends(get_db)):
    p = await db.get(Poll, poll_id)
    if not p: raise HTTPException(404)
    r = await db.execute(select(PollOption).where(PollOption.poll_id == poll_id))
    opts = r.scalars().all()
    total = sum(o.votes_count for o in opts) or 1
    return {"id": p.id, "question": p.question, "is_multiple": p.is_multiple, "expires_at": p.expires_at.isoformat() if p.expires_at else None, "options": [{"id": o.id, "text": o.text, "votes": o.votes_count, "percent": round(o.votes_count / total * 100, 1)} for o in opts]}


@router.post("/polls/{poll_id}/vote")
async def vote_poll(poll_id: int, option_ids: List[int], user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Poll, poll_id)
    if not p: raise HTTPException(404)
    if p.expires_at and p.expires_at < datetime.utcnow(): raise HTTPException(400, "Poll tugagan")
    if not p.is_multiple and len(option_ids) > 1: raise HTTPException(400, "Faqat 1 ta variant")
    
    # Check if already voted
    existing = await db.scalar(select(PollVote).where(PollVote.poll_id == poll_id, PollVote.user_id == user.id))
    if existing and not p.is_multiple: raise HTTPException(400, "Allaqachon ovoz bergan")
    
    for oid in option_ids:
        o = await db.get(PollOption, oid)
        if o and o.poll_id == poll_id:
            o.votes_count += 1
            db.add(PollVote(poll_id=poll_id, option_id=oid, user_id=user.id))
    await db.commit()
    return {"message": "Ovoz berildi"}


# ============ QUIZZES ============
class QuizCreateReq(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str = "medium"  # easy, medium, hard
    questions: List[dict]  # [{question, options, correct, points}]


@router.post("/quizzes")
async def create_quiz(req: QuizCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = Quiz(user_id=user.id, title=req.title, description=req.description, category=req.category, difficulty=req.difficulty)
    db.add(q); await db.commit(); await db.refresh(q)
    for i, qq in enumerate(req.questions):
        db.add(QuizQuestion(quiz_id=q.id, position=i, **qq))
    await db.commit()
    return {"id": q.id, "questions_count": len(req.questions)}


@router.get("/quizzes")
async def list_quizzes(category: Optional[str] = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(Quiz).order_by(Quiz.attempts_count.desc()).limit(limit)
    if category: q = q.where(Quiz.category == category)
    r = await db.execute(q)
    return [{"id": q.id, "title": q.title, "description": q.description, "category": q.category, "difficulty": q.difficulty, "questions_count": q.questions_count, "attempts_count": q.attempts_count} for q in r.scalars().all()]


@router.post("/quizzes/{quiz_id}/start")
async def start_quiz(quiz_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = await db.get(Quiz, quiz_id)
    if not q: raise HTTPException(404)
    attempt = QuizAttempt(quiz_id=quiz_id, user_id=user.id, started_at=datetime.utcnow())
    db.add(attempt); await db.commit(); await db.refresh(attempt)
    
    r = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.position))
    questions = r.scalars().all()
    return {"attempt_id": attempt.id, "questions": [{"id": qq.id, "question": qq.question, "options": qq.options, "points": qq.points} for qq in questions]}


@router.post("/quizzes/attempts/{attempt_id}/submit")
async def submit_quiz(attempt_id: int, answers: dict, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """answers: {question_id: answer}"""
    a = await db.get(QuizAttempt, attempt_id)
    if not a or a.user_id != user.id: raise HTTPException(404)
    
    r = await db.execute(select(QuizQuestion).where(QuizQuestion.quiz_id == a.quiz_id))
    questions = r.scalars().all()
    
    score = 0
    total = 0
    for q in questions:
        total += q.points
        if str(q.id) in answers and answers[str(q.id)] == q.correct:
            score += q.points
    
    a.score = score
    a.total_points = total
    a.percentage = (score / total * 100) if total > 0 else 0
    a.completed_at = datetime.utcnow()
    a.is_passed = a.percentage >= 60
    
    quiz = await db.get(Quiz, a.quiz_id)
    quiz.attempts_count += 1
    
    await db.commit()
    return {"score": score, "total": total, "percentage": a.percentage, "passed": a.is_passed, "xp_earned": int(a.percentage)}
