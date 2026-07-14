"""Chat API - real-time messaging"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Message, Chat, ChatParticipant
from app.api.v1.websocket import manager

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatCreate(BaseModel):
    participant_id: int
    initial_message: Optional[str] = None


class MessageCreate(BaseModel):
    content: str
    type: str = "text"


@router.post("/")
async def create_chat(req: ChatCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Check if chat exists
    existing = await db.execute(
        select(Chat).join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
        .where(and_(
            Chat.is_group == False,
            ChatParticipant.user_id.in_([user.id, req.participant_id])
        )).group_by(Chat.id)
    )
    for chat in existing.scalars():
        # Verify it's between these two users
        participants = await db.execute(
            select(ChatParticipant.user_id).where(ChatParticipant.chat_id == chat.id)
        )
        p_ids = [p[0] for p in participants.all()]
        if set(p_ids) == {user.id, req.participant_id}:
            return {"id": chat.id, "existing": True}

    # Create new chat
    chat = Chat(is_group=False, created_by=user.id)
    db.add(chat)
    await db.flush()
    db.add(ChatParticipant(chat_id=chat.id, user_id=user.id))
    db.add(ChatParticipant(chat_id=chat.id, user_id=req.participant_id))
    
    if req.initial_message:
        msg = Message(chat_id=chat.id, sender_id=user.id, content=req.initial_message, type="text")
        db.add(msg)
    
    await db.commit()
    return {"id": chat.id, "existing": False}


@router.get("/")
async def list_chats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Chat, Message, User)
        .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
        .outerjoin(Message, Message.id == Chat.last_message_id)
        .outerjoin(User, User.id == ChatParticipant.user_id)
        .where(ChatParticipant.user_id == user.id)
        .where(ChatParticipant.user_id != User.id)  # exclude self
        .order_by(Chat.last_message_at.desc().nullslast())
    )
    result = []
    seen = set()
    for chat, msg, other_user in r.all():
        if chat.id in seen: continue
        seen.add(chat.id)
        unread = await db.scalar(
            select(Message.__table__.c.id).where(
                Message.chat_id == chat.id, Message.sender_id != user.id, Message.is_read == False
            )
        )
        result.append({
            "id": chat.id, "other_user": {"id": other_user.id, "full_name": other_user.full_name, "avatar": other_user.avatar_url, "is_online": manager.is_online(other_user.id)},
            "last_message": {"content": msg.content, "created_at": msg.created_at.isoformat()} if msg else None,
            "unread_count": 1 if unread else 0,
            "updated_at": (chat.last_message_at or chat.created_at).isoformat()
        })
    return result


@router.get("/{chat_id}/messages")
async def get_messages(chat_id: int, limit: int = Query(50, le=100), offset: int = 0, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Verify user is participant
    p = await db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user.id))
    if not p: raise HTTPException(403, "Not a participant")
    
    r = await db.execute(select(Message, User).join(User, User.id == Message.sender_id).where(Message.chat_id == chat_id).order_by(Message.created_at.desc()).limit(limit).offset(offset))
    messages = []
    for msg, sender in r.all():
        messages.append({
            "id": msg.id, "content": msg.content, "type": msg.type, "sender_id": msg.sender_id,
            "sender_name": sender.full_name, "sender_avatar": sender.avatar_url,
            "is_mine": msg.sender_id == user.id, "is_read": msg.is_read,
            "created_at": msg.created_at.isoformat()
        })
    return list(reversed(messages))


@router.post("/{chat_id}/messages")
async def send_message(chat_id: int, req: MessageCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user.id))
    if not p: raise HTTPException(403, "Not a participant")
    
    msg = Message(chat_id=chat_id, sender_id=user.id, content=req.content, type=req.type)
    db.add(msg)
    
    # Update chat last message
    chat = await db.get(Chat, chat_id)
    if chat:
        await db.flush()
        chat.last_message_id = msg.id
        chat.last_message_at = datetime.utcnow()
    
    await db.commit()
    
    # Send via WebSocket to other participants
    participants = await db.execute(select(ChatParticipant.user_id).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id != user.id))
    for (other_id,) in participants.all():
        await manager.send_personal(other_id, {
            "type": "new_message", "chat_id": chat_id,
            "message": {"id": msg.id, "content": msg.content, "sender_id": user.id, "sender_name": user.full_name, "created_at": msg.created_at.isoformat()}
        })
    
    return {"id": msg.id, "created_at": msg.created_at.isoformat()}


@router.post("/{chat_id}/read")
async def mark_read(chat_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        Message.__table__.update().where(
            Message.chat_id == chat_id, Message.sender_id != user.id, Message.is_read == False
        ).values(is_read=True)
    )
    await db.commit()
    return {"message": "Marked as read"}


@router.delete("/{chat_id}")
async def delete_chat(chat_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.scalar(select(ChatParticipant).where(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user.id))
    if not p: raise HTTPException(403)
    # Just remove the participant (soft delete)
    await db.delete(p)
    await db.commit()
    return {"message": "Chat o'chirildi"}
