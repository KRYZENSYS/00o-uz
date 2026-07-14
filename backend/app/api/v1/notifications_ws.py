"""Notifications API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Notification, NotificationType, NotificationSetting

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationCreate(BaseModel):
    type: str
    title: str
    message: str
    data: Optional[dict] = None


@router.get("/")
async def list_notifications(unread_only: bool = False, limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Notification).where(Notification.user_id == user.id)
    if unread_only: q = q.where(Notification.is_read == False)
    q = q.order_by(Notification.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": n.id, "type": n.type.value, "title": n.title, "message": n.message, "data": n.data, "is_read": n.is_read, "created_at": n.created_at.isoformat()} for n in r.scalars().all()]


@router.get("/unread-count")
async def unread_count(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    count = await db.scalar(select(func.count(Notification.id)).where(Notification.user_id == user.id, Notification.is_read == False)) or 0
    return {"count": count}


@router.post("/mark-read/{notif_id}")
async def mark_read(notif_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n = await db.get(Notification, notif_id)
    if not n or n.user_id != user.id: raise HTTPException(404)
    n.is_read = True
    n.read_at = func.now() if hasattr(func, 'now') else None
    await db.commit()
    return {"message": "O'qildi"}


@router.post("/mark-all-read")
async def mark_all_read(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        Notification.__table__.update().where(Notification.user_id == user.id, Notification.is_read == False).values(is_read=True)
    )
    await db.commit()
    return {"message": "Hammasi o'qildi"}


@router.delete("/{notif_id}")
async def delete(notif_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n = await db.get(Notification, notif_id)
    if not n or n.user_id != user.id: raise HTTPException(404)
    await db.delete(n); await db.commit()
    return {"message": "O'chirildi"}


@router.post("/clear-all")
async def clear_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(Notification.__table__.delete().where(Notification.user_id == user.id))
    await db.commit()
    return {"message": "Hammasi tozalandi"}


@router.get("/settings")
async def get_settings(user: User = Depends(get_current_user)):
    return {"push_enabled": user.push_enabled, "email_enabled": user.email_enabled, "sms_enabled": user.sms_enabled}


@router.put("/settings")
async def update_settings(push: bool = None, email: bool = None, sms: bool = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if push is not None: user.push_enabled = push
    if email is not None: user.email_enabled = email
    if sms is not None: user.sms_enabled = sms
    await db.commit()
    return {"push_enabled": user.push_enabled, "email_enabled": user.email_enabled, "sms_enabled": user.sms_enabled}


async def create_notification(db: AsyncSession, user_id: int, type: str, title: str, message: str, data: dict = None):
    """Helper to create notification"""
    n = Notification(user_id=user_id, type=NotificationType(type), title=title, message=message, data=data or {})
    db.add(n)
    await db.flush()
    return n
