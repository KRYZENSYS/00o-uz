"""Teams API - team finder, cofounders"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Team, TeamMember, TeamRole, Application, ApplicationStatus

router = APIRouter(prefix="/teams", tags=["teams"])


class TeamCreate(BaseModel):
    name: str
    description: str
    startup_id: Optional[int] = None
    looking_for: List[str] = []
    skills_needed: List[str] = []


class MemberAdd(BaseModel):
    user_id: int
    role: str = "developer"  # developer, designer, marketer, cofounder
    equity: float = 0


@router.get("/")
async def list_teams(search: Optional[str] = None, role: Optional[str] = None, limit: int = Query(50, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Team).where(Team.is_active == True)
    if search: q = q.where(or_(Team.name.ilike(f"%{search}%"), Team.description.ilike(f"%{search}%")))
    q = q.order_by(Team.is_featured.desc(), Team.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": t.id, "name": t.name, "description": t.description, "looking_for": t.looking_for, "skills_needed": t.skills_needed, "members_count": t.members_count, "is_featured": t.is_featured, "created_at": t.created_at.isoformat()} for t in r.scalars().all()]


@router.get("/{team_id}")
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t: raise HTTPException(404)
    r = await db.execute(select(TeamMember, User).join(User, User.id == TeamMember.user_id).where(TeamMember.team_id == team_id))
    members = [{"id": m.user_id, "name": u.full_name, "username": u.username, "avatar": u.avatar_url, "role": m.role.value, "equity": m.equity} for m, u in r.all()]
    return {"id": t.id, "name": t.name, "description": t.description, "looking_for": t.looking_for, "skills_needed": t.skills_needed, "members": members, "members_count": t.members_count, "created_at": t.created_at.isoformat()}


@router.post("/")
async def create_team(req: TeamCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = Team(owner_id=user.id, name=req.name, description=req.description, startup_id=req.startup_id, looking_for=req.looking_for, skills_needed=req.skills_needed, members_count=1)
    db.add(t)
    await db.flush()
    db.add(TeamMember(team_id=t.id, user_id=user.id, role=TeamRole.OWNER, equity=100))
    await db.commit()
    return {"id": t.id}


@router.post("/{team_id}/join")
async def join_team(team_id: int, role: str = "developer", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t: raise HTTPException(404)
    
    existing = await db.scalar(select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id))
    if existing: raise HTTPException(400, "Siz allaqachon a'zosisiz")
    
    # Check if application already exists
    app = await db.scalar(select(Application).where(Application.team_id == team_id, Application.user_id == user.id, Application.status == ApplicationStatus.PENDING))
    if app: raise HTTPException(400, "Arizangiz ko'rib chiqilmoqda")
    
    db.add(Application(team_id=team_id, user_id=user.id, role=role, status=ApplicationStatus.PENDING))
    await db.commit()
    return {"message": "Ariza yuborildi"}


@router.post("/{team_id}/members")
async def add_member(team_id: int, req: MemberAdd, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t or t.owner_id != user.id: raise HTTPException(403)
    db.add(TeamMember(team_id=team_id, user_id=req.user_id, role=TeamRole(req.role), equity=req.equity))
    t.members_count += 1
    await db.commit()
    return {"message": "Qo'shildi"}


@router.get("/{team_id}/applications")
async def list_applications(team_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t or t.owner_id != user.id: raise HTTPException(403)
    r = await db.execute(
        select(Application, User).join(User, User.id == Application.user_id).where(Application.team_id == team_id)
    )
    return [{"id": a.id, "user": {"id": u.id, "name": u.full_name, "username": u.username, "avatar": u.avatar_url}, "role": a.role, "status": a.status.value, "created_at": a.created_at.isoformat()} for a, u in r.all()]


@router.post("/{team_id}/applications/{app_id}/accept")
async def accept_application(team_id: int, app_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t or t.owner_id != user.id: raise HTTPException(403)
    app = await db.get(Application, app_id)
    if not app or app.team_id != team_id: raise HTTPException(404)
    app.status = ApplicationStatus.ACCEPTED
    db.add(TeamMember(team_id=team_id, user_id=app.user_id, role=TeamRole(app.role), equity=0))
    t.members_count += 1
    await db.commit()
    return {"message": "Qabul qilindi"}


@router.post("/{team_id}/applications/{app_id}/reject")
async def reject_application(team_id: int, app_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Team, team_id)
    if not t or t.owner_id != user.id: raise HTTPException(403)
    app = await db.get(Application, app_id)
    if not app or app.team_id != team_id: raise HTTPException(404)
    app.status = ApplicationStatus.REJECTED
    await db.commit()
    return {"message": "Rad etildi"}
