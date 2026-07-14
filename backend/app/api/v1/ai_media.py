"""AI Image/Video/Audio generation"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import os, secrets, asyncio
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, GeneratedMedia

router = APIRouter(prefix="/ai-media", tags=["ai-media"])


class ImageGenReq(BaseModel):
    prompt: str
    model: str = "dall-e-3"  # dall-e-3, midjourney, stable-diffusion
    size: str = "1024x1024"  # 256x256, 512x512, 1024x1024
    style: Optional[str] = "vivid"  # vivid, natural
    quality: str = "standard"  # standard, hd
    n: int = 1


class VideoGenReq(BaseModel):
    prompt: str
    duration: int = 5
    aspect_ratio: str = "16:9"


class AudioGenReq(BaseModel):
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    speed: float = 1.0


@router.post("/image")
async def generate_image(req: ImageGenReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.tokens < 30 and not user.is_premium: raise HTTPException(402, "Token yetarli emas. 30 token kerak.")
    
    # Simulate AI image generation
    os.makedirs("uploads/ai_images", exist_ok=True)
    filename = f"ai_{secrets.token_urlsafe(12)}.jpg"
    
    # In production: call OpenAI DALL-E 3 API
    # For now, return placeholder URL
    media = GeneratedMedia(
        user_id=user.id, type="image", prompt=req.prompt, model=req.model,
        url=f"/uploads/ai_images/{filename}", status="processing"
    )
    db.add(media)
    if not user.is_premium: user.tokens -= 30
    await db.commit()
    await db.refresh(media)
    
    return {"id": media.id, "status": "processing", "url": media.url, "model": req.model}


@router.post("/image/batch")
async def generate_image_batch(prompts: list[str], model: str = "dall-e-3", size: str = "1024x1024", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if len(prompts) > 4: raise HTTPException(400, "Max 4 ta rasm")
    cost = 30 * len(prompts)
    if user.tokens < cost and not user.is_premium: raise HTTPException(402, f"{cost} token kerak")
    
    results = []
    for p in prompts:
        os.makedirs("uploads/ai_images", exist_ok=True)
        filename = f"ai_{secrets.token_urlsafe(12)}.jpg"
        m = GeneratedMedia(user_id=user.id, type="image", prompt=p, model=model, url=f"/uploads/ai_images/{filename}", status="processing")
        db.add(m); results.append({"id": m.id, "prompt": p, "url": m.url})
    if not user.is_premium: user.tokens -= cost
    await db.commit()
    return results


@router.post("/video")
async def generate_video(req: VideoGenReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.tokens < 100 and not user.is_premium: raise HTTPException(402, "100 token kerak")
    m = GeneratedMedia(user_id=user.id, type="video", prompt=req.prompt, model="sora", url="/uploads/ai_videos/pending.mp4", status="processing")
    db.add(m)
    if not user.is_premium: user.tokens -= 100
    await db.commit()
    return {"id": m.id, "status": "processing", "duration": req.duration}


@router.post("/audio/tts")
async def text_to_speech(req: AudioGenReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.tokens < 10 and not user.is_premium: raise HTTPException(402, "10 token kerak")
    m = GeneratedMedia(user_id=user.id, type="audio", prompt=req.text, model=f"tts-{req.voice}", url="/uploads/ai_audio/pending.mp3", status="processing")
    db.add(m)
    if not user.is_premium: user.tokens -= 10
    await db.commit()
    return {"id": m.id, "url": m.url, "voice": req.voice}


@router.get("/gallery")
async def my_gallery(type: Optional[str] = None, limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(GeneratedMedia).where(GeneratedMedia.user_id == user.id)
    if type: q = q.where(GeneratedMedia.type == type)
    q = q.order_by(GeneratedMedia.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": m.id, "type": m.type, "prompt": m.prompt, "url": m.url, "model": m.model, "status": m.status, "created_at": m.created_at.isoformat()} for m in r.scalars().all()]


@router.delete("/{media_id}")
async def delete_media(media_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    m = await db.get(GeneratedMedia, media_id)
    if not m or m.user_id != user.id: raise HTTPException(404)
    await db.delete(m); await db.commit()
    return {"message": "O'chirildi"}


@router.post("/logo")
async def generate_logo(brand_name: str, industry: str, style: str = "modern", colors: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """AI logo generator"""
    if user.tokens < 50 and not user.is_premium: raise HTTPException(402, "50 token kerak")
    prompt = f"Professional logo for {brand_name}, {industry} industry, {style} style, {colors or 'blue and white'} colors, minimalistic, vector, on white background"
    m = GeneratedMedia(user_id=user.id, type="image", prompt=prompt, model="dall-e-3", url="/uploads/ai_images/logo_placeholder.png", status="processing", metadata={"type": "logo", "brand": brand_name})
    db.add(m)
    if not user.is_premium: user.tokens -= 50
    await db.commit()
    return {"id": m.id, "prompt": prompt}


@router.post("/avatar")
async def generate_avatar(style: str = "professional", gender: str = "neutral", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """AI avatar generator for profile"""
    if user.tokens < 30 and not user.is_premium: raise HTTPException(402, "30 token kerak")
    prompt = f"Professional profile photo, {style} style, {gender}, portrait, high quality, 4k"
    m = GeneratedMedia(user_id=user.id, type="image", prompt=prompt, model="dall-e-3", url="/uploads/ai_images/avatar_placeholder.jpg", status="processing", metadata={"type": "avatar"})
    db.add(m)
    if not user.is_premium: user.tokens -= 30
    await db.commit()
    return {"id": m.id, "prompt": prompt}


@router.post("/thumbnail")
async def generate_thumbnail(title: str, style: str = "youtube", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """AI YouTube thumbnail generator"""
    if user.tokens < 40 and not user.is_premium: raise HTTPException(402, "40 token kerak")
    prompt = f"YouTube thumbnail for '{title}', eye-catching, vibrant colors, professional, large text, {style} style"
    m = GeneratedMedia(user_id=user.id, type="image", prompt=prompt, model="dall-e-3", url="/uploads/ai_images/thumb_placeholder.jpg", status="processing", metadata={"type": "thumbnail"})
    db.add(m)
    if not user.is_premium: user.tokens -= 40
    await db.commit()
    return {"id": m.id, "prompt": prompt}
