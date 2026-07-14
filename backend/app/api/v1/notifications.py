"""Notifications API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Notification, NotificationType

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
async def list_notifs(unread_only: bool = False, limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Notification).where(Notification.user_id == user.id)
    if unread_only: q = q.where(Notification.is_read == False)
    q = q.order_by(Notification.created_at.desc()).limit(limit)
    result = await db.execute(q)
    return [{"id": n.id, "type": n.type.value, "title": n.title, "message": n.message,
             "is_read": n.is_read, "created_at": n.created_at.isoformat()} for n in result.scalars().all()]


@router.post("/mark-read/{id}")
async def mark_read(id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n = await db.get(Notification, id)
    if not n or n.user_id != user.id: raise HTTPException(404, "Not found")
    n.is_read = True; n.read_at = datetime.utcnow(); await db.commit()
    return {"ok": True}


@router.post("/mark-all-read")
async def mark_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(update(Notification).where(Notification.user_id == user.id, Notification.is_read == False)
                     .values(is_read=True, read_at=datetime.utcnow()))
    await db.commit()
    return {"ok": True}


@router.get("/unread-count")
async def unread(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.scalar(select(func.count(Notification.id)).where(Notification.user_id == user.id, Notification.is_read == False))
    return {"count": c or 0}


async def send_notification(db: AsyncSession, user_id: int, type: str, title: str, message: str):
    n = Notification(user_id=user_id, type=NotificationType(type), title=title, message=message)
    db.add(n); await db.commit()
    try:
        from app.api.v1.websocket import manager
        await manager.send_personal(user_id, {"type": "notification", "title": title, "message": message})
    except: pass
    return n
