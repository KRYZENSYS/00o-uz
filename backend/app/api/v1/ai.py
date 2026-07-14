"""AI API: Chat, Business Plan, Code, Translation, etc."""
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
import json

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.ai.groq_service import groq_service
from app.models import AIConversation, AIMessage, AILog, User

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    language: str = "uz"
    stream: bool = False


class ToolRequest(BaseModel):
    input: str
    language: str = "uz"
    model: Optional[str] = None


@router.post("/chat")
async def ai_chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """AI Chat with streaming support"""
    start = time.time()
    try:
        messages = [{"role": m.role, "content": m.content} for m in data.messages]

        if data.stream:
            async def generate():
                full = ""
                async for chunk in groq_service._stream_chat(
                    messages, data.model or groq_service.default_model,
                    data.temperature, data.max_tokens, start
                ):
                    if "delta" in chunk:
                        full += chunk["delta"]
                        yield f"data: {json.dumps({'delta': chunk['delta']})}\n\n"
                    elif chunk.get("done"):
                        # Save log
                        duration = int((time.time() - start) * 1000)
                        log = AILog(
                            user_id=current_user.id, tool="chat",
                            model=data.model or groq_service.default_model,
                            total_tokens=len(full.split()),
                            duration_ms=duration, status="success"
                        )
                        db.add(log)
                        await db.commit()
                        yield f"data: {json.dumps({'done': True, 'content': full})}\n\n"

            return StreamingResponse(generate(), media_type="text/event-stream")

        result = await groq_service.chat(
            messages, data.model, data.language, data.temperature, data.max_tokens
        )
        # Log
        log = AILog(
            user_id=current_user.id, tool="chat",
            model=result["model"],
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["tokens"],
            duration_ms=result["duration_ms"],
        )
        db.add(log)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/business-plan")
async def business_plan(data: ToolRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await groq_service.generate_business_plan(data.input, data.language)
    db.add(AILog(user_id=current_user.id, tool="business_plan", model=groq_service.default_model, status="success"))
    await db.commit()
    return {"content": content, "tool": "business_plan"}


@router.post("/startup-ideas")
async def startup_ideas(data: ToolRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await groq_service.generate_startup_ideas(data.input, data.language)
    db.add(AILog(user_id=current_user.id, tool="startup_ideas", model=groq_service.default_model, status="success"))
    await db.commit()
    return {"content": content, "tool": "startup_ideas"}


@router.post("/analyze")
async def analyze(data: ToolRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await groq_service.analyze_startup(data.input, data.language)
    return {"content": content, "tool": "analyze"}


@router.post("/translate")
async def translate(data: ToolRequest, target_language: str = "en", current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await groq_service.translate(data.input, target_language)
    return {"content": content, "tool": "translate"}


@router.post("/summarize")
async def summarize(data: ToolRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await groq_service.summarize(data.input, data.language)
    return {"content": content, "tool": "summarize"}


@router.get("/models")
async def get_models(current_user: User = Depends(get_current_user)):
    return await groq_service.get_models()


@router.get("/history")
async def get_history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AIConversation)
        .where(AIConversation.user_id == current_user.id)
        .order_by(AIConversation.updated_at.desc())
        .limit(50)
    )
    return [
        {
            "id": c.id, "tool": c.tool, "title": c.title,
            "model": c.model, "total_tokens": c.total_tokens,
            "created_at": c.created_at.isoformat(),
        }
        for c in result.scalars().all()
    ]


@router.get("/logs")
async def get_logs(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AILog)
        .where(AILog.user_id == current_user.id)
        .order_by(AILog.created_at.desc())
        .limit(100)
    )
    return [
        {
            "id": l.id, "tool": l.tool, "model": l.model,
            "total_tokens": l.total_tokens, "duration_ms": l.duration_ms,
            "status": l.status, "created_at": l.created_at.isoformat()
        }
        for l in result.scalars().all()
    ]
