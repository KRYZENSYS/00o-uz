"""Voice/Video calls, File sharing, Group calls API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import secrets, os, json

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Call, CallParticipant, FileUpload, GroupCall

router = APIRouter(prefix="/calls", tags=["calls"])


class CallStartReq(BaseModel):
    callee_id: int
    call_type: str = "video"  # audio, video, screen
    is_group: bool = False
    participant_ids: Optional[List[int]] = None


class FileShareReq(BaseModel):
    file_name: str
    file_size: int  # bytes
    file_type: str  # mime type
    chat_id: Optional[int] = None
    conversation_id: Optional[str] = None


@router.post("/start")
async def start_call(req: CallStartReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Start voice/video call (1-1 or group)"""
    if req.is_group and (not req.participant_ids or len(req.participant_ids) > 50): raise HTTPException(400, "2-50 ishtirokchi kerak")
    
    if req.is_group:
        c = GroupCall(caller_id=user.id, call_type=req.call_type, title=f"Group call by {user.full_name}", room_id=secrets.token_urlsafe(16))
        db.add(c); await db.commit(); await db.refresh(c)
        for pid in req.participant_ids:
            db.add(CallParticipant(call_id=c.id, user_id=pid))
        await db.commit()
        return {"id": c.id, "room_id": c.room_id, "is_group": True, "webrtc_offer": {"type": "offer", "sdp": "placeholder"}}
    else:
        c = Call(caller_id=user.id, callee_id=req.callee_id, call_type=req.call_type, room_id=secrets.token_urlsafe(16), status="ringing")
        db.add(c); await db.commit(); await db.refresh(c)
        return {"id": c.id, "room_id": c.room_id, "is_group": False}


@router.post("/{call_id}/accept")
async def accept_call(call_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Call, call_id)
    if not c or c.callee_id != user.id: raise HTTPException(403)
    c.status = "ongoing"
    c.started_at = datetime.utcnow()
    await db.commit()
    return {"message": "Qabul qilindi", "room_id": c.room_id}


@router.post("/{call_id}/reject")
async def reject_call(call_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Call, call_id)
    if not c or c.callee_id != user.id: raise HTTPException(403)
    c.status = "rejected"
    c.ended_at = datetime.utcnow()
    await db.commit()
    return {"message": "Rad etildi"}


@router.post("/{call_id}/end")
async def end_call(call_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Call, call_id)
    if c and (c.caller_id == user.id or c.callee_id == user.id):
        c.status = "ended"
        c.ended_at = datetime.utcnow()
        await db.commit()
    return {"message": "Tugadi"}


@router.get("/history")
async def call_history(limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Call).where((Call.caller_id == user.id) | (Call.callee_id == user.id))
        .order_by(Call.created_at.desc()).limit(limit)
    )
    return [{"id": c.id, "type": c.call_type, "status": c.status, "duration": c.duration, "created_at": c.created_at.isoformat()} for c in r.scalars().all()]


# ============ FILE SHARING ============
@router.post("/files/upload-url")
async def get_upload_url(req: FileShareReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get presigned URL for file upload (S3/MinIO)"""
    if req.file_size > 50 * 1024 * 1024: raise HTTPException(400, "Max 50MB")
    
    file_id = secrets.token_urlsafe(16)
    file = FileUpload(id=file_id, user_id=user.id, file_name=req.file_name, file_size=req.file_size, file_type=req.file_type, status="uploading")
    db.add(file); await db.commit()
    
    return {
        "file_id": file_id,
        "upload_url": f"https://upload.00o.uz/files/{file_id}",
        "download_url": f"https://files.00o.uz/{file_id}/{req.file_name}"
    }


@router.get("/files/my")
async def my_files(limit: int = 100, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(FileUpload).where(FileUpload.user_id == user.id).order_by(FileUpload.created_at.desc()).limit(limit))
    return [{"id": f.id, "file_name": f.file_name, "file_size": f.file_size, "file_type": f.file_type, "download_url": f"https://files.00o.uz/{f.id}/{f.file_name}", "created_at": f.created_at.isoformat()} for f in r.scalars().all()]


@router.delete("/files/{file_id}")
async def delete_file(file_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    f = await db.get(FileUpload, file_id)
    if not f or f.user_id != user.id: raise HTTPException(404)
    await db.delete(f); await db.commit()
    return {"message": "O'chirildi"}


# ============ CONFERENCE / WEBINAR ============
@router.post("/conference/create")
async def create_conference(title: str, scheduled_for: datetime, max_participants: int = 100, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Create a video conference (Zoom-like)"""
    c = GroupCall(caller_id=user.id, call_type="conference", title=title, room_id=secrets.token_urlsafe(16), max_participants=max_participants, scheduled_for=scheduled_for)
    db.add(c); await db.commit(); await db.refresh(c)
    return {"id": c.id, "room_id": c.room_id, "join_url": f"https://00o.uz/call/{c.room_id}"}
