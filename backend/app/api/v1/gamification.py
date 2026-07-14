"""Gamification - XP, Badges, Levels, Missions, Leaderboard"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, UserXP, Badge, UserBadge, Mission, UserMission, Leaderboard

router = APIRouter(prefix="/game", tags=["gamification"])


LEVELS = [
    {"level": 1, "xp_required": 0, "name": "Yangi boshlovchi", "color": "gray"},
    {"level": 2, "xp_required": 100, "name": "Faol a'zo", "color": "green"},
    {"level": 3, "xp_required": 300, "name": "Tajribali", "color": "blue"},
    {"level": 4, "xp_required": 700, "name": "Professional", "color": "purple"},
    {"level": 5, "xp_required": 1500, "name": "Ekspert", "color": "orange"},
    {"level": 6, "xp_required": 3000, "name": "Usta", "color": "red"},
    {"level": 7, "xp_required": 6000, "name": "Guru", "color": "yellow"},
    {"level": 8, "xp_required": 12000, "name": "Afsona", "color": "pink"},
    {"level": 9, "xp_required": 25000, "name": "Mister 00o", "color": "cyan"},
    {"level": 10, "xp_required": 50000, "name": "00o Champion", "color": "rainbow"},
]


BADGES = [
    {"id": "first_startup", "name": "Birinchi startap", "icon": "🚀", "desc": "Birinchi startap yaratdingiz", "xp": 50, "color": "blue"},
    {"id": "first_job", "name": "Birinchi ish", "icon": "💼", "desc": "Birinchi vakansiya joyladingiz", "xp": 30, "color": "green"},
    {"id": "first_service", "name": "Birinchi xizmat", "icon": "🛠️", "desc": "Birinchi xizmat yaratdingiz", "xp": 30, "color": "yellow"},
    {"id": "ai_master", "name": "AI ustasi", "icon": "🤖", "desc": "100 ta AI so'rov yubordingiz", "xp": 200, "color": "purple"},
    {"id": "social_butterfly", "name": "Ijtimoiy kapalak", "icon": "🦋", "desc": "1000 ta follower to'pladingiz", "xp": 300, "color": "pink"},
    {"id": "verified", "name": "Tasdiqlangan", "icon": "✓", "desc": "Verified badge oldingiz", "xp": 100, "color": "blue"},
    {"id": "premium_member", "name": "Premium a'zo", "icon": "👑", "desc": "Premium sotib oldingiz", "xp": 150, "color": "yellow"},
    {"id": "early_adopter", "name": "Erta foydalanuvchi", "icon": "⭐", "desc": "00o.uz ning 1000 ta foydalanuvchisi bo'ldingiz", "xp": 500, "color": "orange"},
    {"id": "founder", "name": "Asoschi", "icon": "👨‍💼", "desc": "Co-founder kerakli startap yaratdingiz", "xp": 80, "color": "indigo"},
    {"id": "investor", "name": "Investor", "icon": "💰", "desc": "Investor profili yaratdingiz", "xp": 80, "color": "green"},
    {"id": "mentor", "name": "Mentor", "icon": "🎓", "desc": "10 kishiga yordam berdingiz", "xp": 200, "color": "purple"},
    {"id": "creator", "name": "Yaratuvchi", "icon": "✍️", "desc": "50 ta post yozdingiz", "xp": 150, "color": "rose"},
    {"id": "streamer", "name": "Strimer", "icon": "📹", "desc": "Birinchi live stream o'tkazdingiz", "xp": 100, "color": "red"},
    {"id": "teacher", "name": "O'qituvchi", "icon": "👨‍🏫", "desc": "Birinchi kurs yaratdingiz", "xp": 200, "color": "indigo"},
    {"id": "helper", "name": "Yordamchi", "icon": "🤝", "desc": "100 kishiga yordam berdingiz", "xp": 300, "color": "teal"},
]


@router.get("/me")
async def my_profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    xp = user.xp or 0
    current_level = LEVELS[0]
    next_level = LEVELS[1] if len(LEVELS) > 1 else None
    for i, lv in enumerate(LEVELS):
        if xp >= lv["xp_required"]:
            current_level = lv
            next_level = LEVELS[i + 1] if i + 1 < len(LEVELS) else None
    progress = 100 if not next_level else ((xp - current_level["xp_required"]) / (next_level["xp_required"] - current_level["xp_required"])) * 100
    
    # Get badges
    r = await db.execute(select(UserBadge, Badge).join(Badge, Badge.id == UserBadge.badge_id).where(UserBadge.user_id == user.id))
    badges = [{"id": b.id, "name": b.name, "icon": b.icon, "desc": b.desc, "color": b.color, "earned_at": ub.earned_at.isoformat()} for ub, b in r.all()]
    
    # Get rank
    rank = await db.scalar(select(func.count(User.id)).where(User.xp > xp)) or 0
    
    return {
        "xp": xp, "level": current_level, "next_level": next_level, "progress": round(progress, 1),
        "rank": rank + 1, "badges": badges, "badges_total": len(BADGES), "streak_days": user.streak_days or 0
    }


@router.post("/xp/add")
async def add_xp(amount: int, reason: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.xp = (user.xp or 0) + amount
    await db.commit()
    return {"xp": user.xp, "added": amount, "reason": reason}


@router.get("/badges")
async def all_badges():
    return BADGES


@router.get("/leaderboard")
async def leaderboard(period: str = "all", limit: int = 100, db: AsyncSession = Depends(get_db)):
    q = select(User).where(User.is_active == True).order_by(User.xp.desc().nullslast()).limit(limit)
    r = await db.execute(q)
    return [{"rank": i + 1, "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "xp": u.xp, "level": next((lv["level"] for lv in reversed(LEVELS) if (u.xp or 0) >= lv["xp_required"]), 1)}} for i, u in enumerate(r.scalars().all())]


@router.get("/missions")
async def daily_missions(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Daily missions"""
    today = datetime.utcnow().date()
    r = await db.execute(select(UserMission).where(UserMission.user_id == user.id, UserMission.date == today))
    completed = {m.mission_id: m for m in r.scalars().all()}
    missions = [
        {"id": "login", "name": "Tizimga kirish", "desc": "Bugun kirib oling", "reward": 10, "progress": 1 if "login" in completed else 0, "target": 1, "completed": "login" in completed},
        {"id": "ai_5", "name": "AI ishlating", "desc": "5 ta AI so'rov yuboring", "reward": 30, "progress": completed.get("ai_5").progress if "ai_5" in completed else 0, "target": 5, "completed": "ai_5" in completed and completed["ai_5"].progress >= 5},
        {"id": "post_1", "name": "Post yozing", "desc": "1 ta post joylang", "reward": 20, "progress": 1 if "post_1" in completed else 0, "target": 1, "completed": "post_1" in completed},
        {"id": "comment_3", "name": "Faol bo'ling", "desc": "3 ta izoh yozing", "reward": 25, "progress": completed.get("comment_3").progress if "comment_3" in completed else 0, "target": 3, "completed": "comment_3" in completed and completed["comment_3"].progress >= 3},
        {"id": "like_5", "name": "Yoqtiring", "desc": "5 ta post yoqtiring", "reward": 15, "progress": completed.get("like_5").progress if "like_5" in completed else 0, "target": 5, "completed": "like_5" in completed and completed["like_5"].progress >= 5},
    ]
    return missions


@router.post("/missions/{mission_id}/complete")
async def complete_mission(mission_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    today = datetime.utcnow().date()
    existing = await db.scalar(select(UserMission).where(UserMission.user_id == user.id, UserMission.mission_id == mission_id, UserMission.date == today))
    if existing and existing.completed: raise HTTPException(400, "Allaqachon bajarilgan")
    
    rewards = {"login": 10, "ai_5": 30, "post_1": 20, "comment_3": 25, "like_5": 15}
    reward = rewards.get(mission_id, 10)
    
    if existing: existing.completed = True; existing.progress = existing.target
    else: db.add(UserMission(user_id=user.id, mission_id=mission_id, date=today, completed=True, progress=1, target=1))
    
    user.xp = (user.xp or 0) + reward
    user.streak_days = (user.streak_days or 0) + 1 if mission_id == "login" else user.streak_days
    await db.commit()
    return {"xp_earned": reward, "total_xp": user.xp}


@router.get("/streak")
async def my_streak(user: User = Depends(get_current_user)):
    return {"days": user.streak_days or 0, "next_reward": 50 if (user.streak_days or 0) % 7 == 6 else None}
