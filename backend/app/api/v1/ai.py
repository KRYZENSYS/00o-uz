"""AI API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, AIRequest
from app.ai.tools import TOOLS_MAP

router = APIRouter(prefix="/ai", tags=["ai"])


class AIExecuteReq(BaseModel):
    tool: str
    input: str
    language: str = "uz"
    max_tokens: int = 4000


@router.get("/tools")
async def list_tools():
    """List all available AI tools"""
    return [
        {"id": "chat", "name": "AI Chat", "category": "general", "icon": "💬", "desc": "Umumiy suhbat"},
        {"id": "business-plan", "name": "Biznes reja", "category": "business", "icon": "📋", "desc": "Professional biznes reja"},
        {"id": "pitch-deck", "name": "Pitch deck", "category": "business", "icon": "🎯", "desc": "Investor uchun taqdimot"},
        {"id": "startup-ideas", "name": "Startap g'oyalar", "category": "business", "icon": "💡", "desc": "Kreativ g'oyalar"},
        {"id": "swot", "name": "SWOT tahlil", "category": "analysis", "icon": "📊", "desc": "Tahlil"},
        {"id": "business-name", "name": "Biznes nomi", "category": "business", "icon": "🏷️", "desc": "Kreativ nomlar"},
        {"id": "logo-prompt", "name": "Logo prompt", "category": "design", "icon": "🎨", "desc": "AI logotip"},
        {"id": "domain", "name": "Domen nomi", "category": "business", "icon": "🌐", "desc": "Domenlar"},
        {"id": "resume", "name": "Resume", "category": "career", "icon": "📄", "desc": "Professional CV"},
        {"id": "cover-letter", "name": "Cover Letter", "category": "career", "icon": "✉️", "desc": "Motivatsion xat"},
        {"id": "job-description", "name": "Ish tavsifi", "category": "career", "icon": "💼", "desc": "JD yozish"},
        {"id": "marketing", "name": "Marketing", "category": "marketing", "icon": "📈", "desc": "Strategiya"},
        {"id": "seo", "name": "SEO", "category": "marketing", "icon": "🔍", "desc": "Qidiruv optimallashtirish"},
        {"id": "blog", "name": "Blog post", "category": "content", "icon": "📝", "desc": "Maqola yozish"},
        {"id": "social", "name": "Ijtimoiy tarmoq", "category": "content", "icon": "📱", "desc": "SM kontent"},
        {"id": "email", "name": "Email", "category": "content", "icon": "✉️", "desc": "Professional email"},
        {"id": "code", "name": "Kod", "category": "code", "icon": "💻", "desc": "Dasturlash"},
        {"id": "fix-bug", "name": "Bug fix", "category": "code", "icon": "🐛", "desc": "Xatolarni tuzatish"},
        {"id": "code-review", "name": "Code review", "category": "code", "icon": "👀", "desc": "Kod tekshirish"},
        {"id": "api-docs", "name": "API docs", "category": "code", "icon": "📚", "desc": "Hujjatlashtirish"},
        {"id": "sql", "name": "SQL", "category": "code", "icon": "🗄️", "desc": "Database so'rovlar"},
        {"id": "ui", "name": "UI komponent", "category": "code", "icon": "🎨", "desc": "Interfeys"},
        {"id": "summarize", "name": "Xulosa", "category": "general", "icon": "📋", "desc": "Qisqartirish"},
        {"id": "brainstorm", "name": "Brainstorm", "category": "general", "icon": "💡", "desc": "G'oyalar"},
        {"id": "planner", "name": "Planner", "category": "general", "icon": "📅", "desc": "Loyiha rejasi"},
        {"id": "financial", "name": "Moliyaviy", "category": "analysis", "icon": "💰", "desc": "Moliyaviy tahlil"},
        {"id": "market", "name": "Bozor", "category": "analysis", "icon": "📊", "desc": "Bozor tadqiqoti"},
        {"id": "competitor", "name": "Raqobatchi", "category": "analysis", "icon": "🎯", "desc": "Raqobatchilar"},
        {"id": "legal", "name": "Yuridik", "category": "analysis", "icon": "⚖️", "desc": "Yuridik maslahat"},
        {"id": "translate", "name": "Tarjimon", "category": "language", "icon": "🌍", "desc": "100+ til"},
    ]


@router.post("/execute")
async def execute(req: AIExecuteReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if req.tool not in TOOLS_MAP: raise HTTPException(400, f"Tool '{req.tool}' topilmadi")
    
    # Check tokens
    if user.tokens < 5 and not user.is_premium: raise HTTPException(402, "Token yetarli emas. Premium yoki token sotib oling.")
    
    # Execute
    tool_func = TOOLS_MAP[req.tool]
    try:
        if req.tool == "translate":
            output = await tool_func(req.input, req.language)
        else:
            output = await tool_func(req.input, req.language)
    except Exception as e:
        output = f"Xatolik: {str(e)}"
    
    # Save to history
    tokens_used = len(req.input) + len(output)
    ai_req = AIRequest(user_id=user.id, tool=req.tool, input=req.input, output=output, tokens_used=tokens_used // 4)
    db.add(ai_req)
    
    # Deduct tokens
    if not user.is_premium:
        user.tokens = max(0, user.tokens - max(1, tokens_used // 100))
    
    await db.commit()
    
    return {"tool": req.tool, "output": output, "tokens_used": tokens_used // 4, "remaining_tokens": user.tokens}


@router.get("/history")
async def history(limit: int = 50, tool: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(AIRequest).where(AIRequest.user_id == user.id)
    if tool: q = q.where(AIRequest.tool == tool)
    q = q.order_by(AIRequest.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": h.id, "tool": h.tool, "input": h.input[:200], "output": h.output[:500] if h.output else "", "tokens_used": h.tokens_used, "created_at": h.created_at.isoformat()} for h in r.scalars().all()]


@router.delete("/history/{req_id}")
async def delete_history(req_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    h = await db.get(AIRequest, req_id)
    if not h or h.user_id != user.id: raise HTTPException(404)
    await db.delete(h); await db.commit()
    return {"message": "O'chirildi"}


@router.post("/history/clear")
async def clear_history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(AIRequest.__table__.delete().where(AIRequest.user_id == user.id))
    await db.commit()
    return {"message": "Tarix tozalandi"}


@router.get("/usage")
async def my_usage(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(AIRequest.tool, func.count(AIRequest.id), func.sum(AIRequest.tokens_used))
        .where(AIRequest.user_id == user.id).group_by(AIRequest.tool).order_by(func.count(AIRequest.id).desc())
    )
    return [{"tool": t, "count": c, "tokens": tk or 0} for t, c, tk in r.all()]
