"""Stories API - Instagram-like 24h stories"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import os, secrets, shutil

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Story, StoryView

router = APIRouter(prefix="/stories", tags=["stories"])


class StoryCreate(BaseModel):
    media_type: str  # image, video, text
    media_url: Optional[str] = None
    text: Optional[str] = None
    background_color: Optional[str] = "#000000"
    duration: int = 5


@router.get("/")
async def list_stories(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cutoff = datetime.utcnow() - timedelta(hours=24)
    r = await db.execute(
        select(Story, User).join(User, User.id == Story.user_id)
        .where(Story.created_at > cutoff, Story.is_hidden == False)
        .order_by(Story.created_at.desc())
    )
    result = []
    seen_users = {}
    for s, u in r.all():
        uid = u.id
        if uid not in seen_users:
            seen_users[uid] = {"user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_verified": u.is_verified, "is_premium": u.is_premium}, "stories": [], "has_viewed": False}
        seen_users[uid]["stories"].append({"id": s.id, "media_type": s.media_type, "media_url": s.media_url, "text": s.text, "background_color": s.background_color, "views_count": s.views_count, "created_at": s.created_at.isoformat()})
    return list(seen_users.values())


@router.post("/")
async def create_story(req: StoryCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = Story(user_id=user.id, media_type=req.media_type, media_url=req.media_url, text=req.text, background_color=req.background_color, duration=req.duration, expires_at=datetime.utcnow() + timedelta(hours=24))
    db.add(s); await db.commit(); await db.refresh(s)
    return {"id": s.id, "expires_at": s.expires_at.isoformat()}


@router.post("/{story_id}/view")
async def view_story(story_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(Story, story_id)
    if not s or s.is_hidden: raise HTTPException(404)
    existing = await db.scalar(select(StoryView).where(StoryView.story_id == story_id, StoryView.user_id == user.id))
    if not existing:
        db.add(StoryView(story_id=story_id, user_id=user.id))
        s.views_count += 1
        await db.commit()
    return {"views": s.views_count}


@router.get("/{story_id}/viewers")
async def viewers(story_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(Story, story_id)
    if not s or s.user_id != user.id: raise HTTPException(403)
    r = await db.execute(select(StoryView, User).join(User, User.id == StoryView.user_id).where(StoryView.story_id == story_id).order_by(StoryView.viewed_at.desc()))
    return [{"id": sv.id, "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url}, "viewed_at": sv.viewed_at.isoformat()} for sv, u in r.all()]


@router.delete("/{story_id}")
async def delete_story(story_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(Story, story_id)
    if not s or s.user_id != user.id: raise HTTPException(403)
    s.is_hidden = True
    await db.commit()
    return {"message": "O'chirildi"}


@router.post("/upload")
async def upload_story(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    """Upload story media"""
    os.makedirs("uploads/stories", exist_ok=True)
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    fname = f"{secrets.token_urlsafe(16)}.{ext}"
    path = f"uploads/stories/{fname}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/uploads/stories/{fname}", "type": "image" if ext in ["jpg", "jpeg", "png", "webp"] else "video"}
