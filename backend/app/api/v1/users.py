"""Users API - user profile, search, follow"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from pydantic import BaseModel
from typing import Optional
import os
import uuid

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Follow, Notification, NotificationType

router = APIRouter(prefix="/users", tags=["users"])


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None


@router.get("/me/stats")
async def my_stats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    followers = await db.scalar(select(func.count(Follow.id)).where(Follow.following_id == user.id)) or 0
    following = await db.scalar(select(func.count(Follow.id)).where(Follow.follower_id == user.id)) or 0
    startups = await db.scalar(select(func.count(User.id)).where(User.id == user.id)) or 0  # count from startup table
    return {"followers": followers, "following": following, "startups": 0, "services": 0, "posts": 0}


@router.put("/me")
async def update_me(req: UserUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    for field, value in req.dict(exclude_unset=True).items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    await db.commit()
    return {"id": user.id, "full_name": user.full_name, "bio": user.bio, "phone": user.phone, "avatar_url": user.avatar_url}


@router.post("/me/avatar")
async def upload_avatar(file: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    os.makedirs("uploads/avatars", exist_ok=True)
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    path = f"uploads/avatars/{filename}"
    with open(path, "wb") as f: f.write(await file.read())
    user.avatar_url = f"/uploads/avatars/{filename}"
    await db.commit()
    return {"url": user.avatar_url}


@router.get("/search")
async def search_users(q: str = Query(min_length=1), limit: int = Query(20, le=50), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(User).where(or_(User.username.ilike(f"%{q}%"), User.full_name.ilike(f"%{q}%")))
        .where(User.is_active == True).limit(limit)
    )
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "bio": u.bio, "is_premium": u.is_premium, "is_verified": u.is_verified} for u in r.scalars().all()]


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    u = await db.get(User, user_id)
    if not u or not u.is_active: raise HTTPException(404)
    followers = await db.scalar(select(func.count(Follow.id)).where(Follow.following_id == u.id)) or 0
    following = await db.scalar(select(func.count(Follow.id)).where(Follow.follower_id == u.id)) or 0
    return {
        "id": u.id, "username": u.username, "full_name": u.full_name, "bio": u.bio, "avatar_url": u.avatar_url,
        "is_verified": u.is_verified, "is_premium": u.is_premium, "role": u.role.value,
        "company": u.company if hasattr(u, 'company') else None, "position": u.position if hasattr(u, 'position') else None,
        "website": u.website if hasattr(u, 'website') else None, "followers": followers, "following": following,
        "created_at": u.created_at.isoformat()
    }


@router.post("/{user_id}/follow")
async def follow_user(user_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user_id == user.id: raise HTTPException(400, "O'zingizni follow qila olmaysiz")
    target = await db.get(User, user_id)
    if not target: raise HTTPException(404)
    
    existing = await db.scalar(select(Follow).where(Follow.follower_id == user.id, Follow.following_id == user_id))
    if existing:
        await db.delete(existing)
        await db.commit()
        return {"following": False}
    
    db.add(Follow(follower_id=user.id, following_id=user_id))
    
    # Create notification
    db.add(Notification(
        user_id=user_id, type=NotificationType.FOLLOW,
        title="Yangi obunachi", message=f"{user.full_name} sizga obuna bo'ldi",
        data={"from_user_id": user.id}
    ))
    
    await db.commit()
    return {"following": True}


@router.get("/{user_id}/followers")
async def get_followers(user_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(User).join(Follow, Follow.follower_id == User.id).where(Follow.following_id == user_id)
    )
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_premium": u.is_premium} for u in r.scalars().all()]


@router.get("/{user_id}/following")
async def get_following(user_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(User).join(Follow, Follow.following_id == User.id).where(Follow.follower_id == user_id)
    )
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_premium": u.is_premium} for u in r.scalars().all()]
