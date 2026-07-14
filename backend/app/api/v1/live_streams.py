"""Live Streaming API - WebRTC based"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, LiveStream, StreamViewer, StreamChat

router = APIRouter(prefix="/streams", tags=["live-streams"])


class StreamStartReq(BaseModel):
    title: str
    description: Optional[str] = None
    category: str = "general"
    thumbnail: Optional[str] = None
    is_private: bool = False


class StreamChatReq(BaseModel):
    message: str


@router.get("/live")
async def live_streams(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(LiveStream, User).join(User, User.id == LiveStream.user_id).where(LiveStream.is_live == True, LiveStream.ended_at == None).order_by(LiveStream.viewers_count.desc()))
    return [{"id": s.id, "title": s.title, "description": s.description, "category": s.category, "thumbnail": s.thumbnail, "viewers": s.viewers_count, "started_at": s.started_at.isoformat(), "streamer": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_verified": u.is_verified}} for s, u in r.all()]


@router.get("/upcoming")
async def upcoming_streams(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(LiveStream, User).join(User, User.id == LiveStream.user_id).where(LiveStream.is_live == False, LiveStream.scheduled_for > datetime.utcnow()).order_by(LiveStream.scheduled_for).limit(20))
    return [{"id": s.id, "title": s.title, "category": s.category, "thumbnail": s.thumbnail, "scheduled_for": s.scheduled_for.isoformat() if s.scheduled_for else None, "streamer": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url}} for s, u in r.all()]


@router.post("/start")
async def start_stream(req: StreamStartReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = LiveStream(user_id=user.id, title=req.title, description=req.description, category=req.category, thumbnail=req.thumbnail, is_private=req.is_private, is_live=True, started_at=datetime.utcnow())
    db.add(s); await db.commit(); await db.refresh(s)
    return {"id": s.id, "stream_key": f"sk_{s.id}_{user.id}", "rtmp_url": "rtmps://live.00o.uz/live", "playback_url": f"https://stream.00o.uz/{s.id}/playlist.m3u8"}


@router.post("/{stream_id}/end")
async def end_stream(stream_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(LiveStream, stream_id)
    if not s or s.user_id != user.id: raise HTTPException(403)
    s.is_live = False
    s.ended_at = datetime.utcnow()
    await db.commit()
    return {"message": "Stream tugadi"}


@router.post("/{stream_id}/join")
async def join_stream(stream_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(LiveStream, stream_id)
    if not s or not s.is_live: raise HTTPException(404)
    existing = await db.scalar(select(StreamViewer).where(StreamViewer.stream_id == stream_id, StreamViewer.user_id == user.id))
    if not existing:
        db.add(StreamViewer(stream_id=stream_id, user_id=user.id))
        s.viewers_count += 1
        await db.commit()
    return {"playback_url": f"https://stream.00o.uz/{stream_id}/playlist.m3u8", "viewers": s.viewers_count}


@router.post("/{stream_id}/leave")
async def leave_stream(stream_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.get(LiveStream, stream_id)
    if s:
        v = await db.scalar(select(StreamViewer).where(StreamViewer.stream_id == stream_id, StreamViewer.user_id == user.id))
        if v:
            await db.delete(v)
            s.viewers_count = max(0, s.viewers_count - 1)
            await db.commit()
    return {"message": "Chiqildi"}


@router.get("/{stream_id}/chat")
async def get_chat(stream_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(StreamChat, User).join(User, User.id == StreamChat.user_id).where(StreamChat.stream_id == stream_id).order_by(StreamChat.created_at.desc()).limit(100))
    return [{"id": c.id, "message": c.message, "created_at": c.created_at.isoformat(), "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_premium": u.is_premium}} for c, u in r.all()]


@router.post("/{stream_id}/chat")
async def post_chat(stream_id: int, req: StreamChatReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = StreamChat(stream_id=stream_id, user_id=user.id, message=req.message[:500])
    db.add(c); await db.commit()
    return {"id": c.id, "message": c.message}


@router.post("/{stream_id}/donate")
async def donate(stream_id: int, amount: int, message: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Donate to streamer"""
    if amount < 1000: raise HTTPException(400, "Minimal 1000 so'm")
    if user.tokens < amount // 100: raise HTTPException(402, "Token yetarli emas")
    
    s = await db.get(LiveStream, stream_id)
    if not s: raise HTTPException(404)
    
    s.donations_total = (s.donations_total or 0) + amount
    user.tokens -= amount // 100
    await db.commit()
    
    # Add to chat as special message
    db.add(StreamChat(stream_id=stream_id, user_id=user.id, message=f"💰 {amount} so'm donation: {message or ''}"))
    await db.commit()
    
    return {"message": "Donation yuborildi", "new_total": s.donations_total}


@router.post("/schedule")
async def schedule_stream(title: str, description: str, scheduled_for: datetime, category: str = "general", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Schedule a future stream"""
    s = LiveStream(user_id=user.id, title=title, description=description, category=category, scheduled_for=scheduled_for, is_live=False)
    db.add(s); await db.commit()
    return {"id": s.id, "scheduled_for": s.scheduled_for.isoformat()}
