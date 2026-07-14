"""AI API - 30+ tools"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, AIRequest
from app.ai import tools as ai_tools
from sqlalchemy import select

router = APIRouter(prefix="/ai", tags=["ai"])


class AIRequestModel(BaseModel):
    tool: str
    input: str
    language: str = "uz"
    target_lang: Optional[str] = "en"


@router.post("/execute")
async def execute(req: AIRequestModel, user: User = Depends(get_current_user), db = Depends(get_db)):
    start = time.time()
    if req.tool not in ai_tools.TOOLS_MAP: raise HTTPException(400, "Unknown tool")
    cost = 0 if user.is_premium else 10
    if user.tokens < cost: raise HTTPException(402, f"Token yetarli emas: {cost}")

    tool_func = ai_tools.TOOLS_MAP[req.tool]
    content = await tool_func(req.input, req.target_lang) if req.tool == "translate" else await tool_func(req.input, req.language)

    if cost > 0: user.tokens -= cost
    db.add(AIRequest(user_id=user.id, tool=req.tool, input=req.input, output=content, tokens_used=cost))
    await db.commit()
    return {"tool": req.tool, "content": content, "tokens_used": cost, "time": round(time.time()-start, 2)}


@router.get("/tools")
async def list_tools():
    return [
        {"id": t, "name": t.replace("-", " ").title(), "cost": 0 if i < 3 else 10}
        for i, t in enumerate(ai_tools.TOOLS_MAP.keys())
    ]


@router.get("/history")
async def history(limit: int = 50, user: User = Depends(get_current_user), db = Depends(get_db)):
    result = await db.execute(select(AIRequest).where(AIRequest.user_id == user.id)
                              .order_by(AIRequest.created_at.desc()).limit(limit))
    return [{"id": r.id, "tool": r.tool, "input": r.input[:100], "output": r.output[:200], "created_at": r.created_at.isoformat()}
            for r in result.scalars().all()]
