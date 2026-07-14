"""Posts/Feed API - social feed"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Post, Comment, Like, Notification, NotificationType, Follow

router = APIRouter(prefix="/posts", tags=["posts"])


class PostCreate(BaseModel):
    content: str
    images: List[str] = []
    tags: List[str] = []
    visibility: str = "public"  # public, followers, private


class CommentCreate(BaseModel):
    content: str


@router.get("/feed")
async def feed(limit: int = Query(20, le=50), offset: int = 0, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Posts from users I follow + my own
    following = await db.execute(select(Follow.following_id).where(Follow.follower_id == user.id))
    following_ids = [f[0] for f in following.all()] + [user.id]
    
    r = await db.execute(
        select(Post, User).join(User, User.id == Post.user_id)
        .where(Post.user_id.in_(following_ids))
        .where(Post.visibility == "public")
        .order_by(Post.created_at.desc())
        .limit(limit).offset(offset)
    )
    return await _format_posts(r.all(), user, db)


@router.get("/trending")
async def trending(limit: int = 20, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Post, User).join(User, User.id == Post.user_id)
        .where(Post.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0))
        .order_by((Post.likes_count + Post.comments_count * 2).desc())
        .limit(limit)
    )
    return await _format_posts(r.all(), None, db)


@router.get("/user/{user_id}")
async def user_posts(user_id: int, limit: int = Query(20, le=50), offset: int = 0, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(Post, User).join(User, User.id == Post.user_id)
        .where(Post.user_id == user_id)
        .where(Post.visibility.in_(["public", "followers"]))
        .order_by(Post.created_at.desc())
        .limit(limit).offset(offset)
    )
    return await _format_posts(r.all(), None, db)


async def _format_posts(posts_data, current_user, db):
    result = []
    for p, u in posts_data:
        liked = False
        if current_user:
            liked = await db.scalar(select(Like).where(Like.user_id == current_user.id, Like.target_type == "post", Like.target_id == p.id)) is not None
        result.append({
            "id": p.id, "content": p.content, "images": p.images or [], "tags": p.tags or [],
            "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_premium": u.is_premium, "is_verified": u.is_verified},
            "likes_count": p.likes_count, "comments_count": p.comments_count, "shares_count": p.shares_count, "views_count": p.views_count,
            "is_liked": liked, "visibility": p.visibility, "created_at": p.created_at.isoformat()
        })
    return result


@router.post("/")
async def create_post(req: PostCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = Post(user_id=user.id, content=req.content, images=req.images, tags=req.tags, visibility=req.visibility)
    db.add(p)
    await db.commit()
    return {"id": p.id, "created_at": p.created_at.isoformat()}


@router.get("/{post_id}")
async def get_post(post_id: int, user: User = Depends(get_current_user) = None, db: AsyncSession = Depends(get_db)):
    p = await db.get(Post, post_id)
    if not p: raise HTTPException(404)
    
    p.views_count += 1
    if user and user.id != p.user_id:
        await db.commit()
    
    u = await db.get(User, p.user_id)
    r = await db.execute(
        select(Comment, User).join(User, User.id == Comment.user_id)
        .where(Comment.post_id == post_id).order_by(Comment.created_at.asc())
    )
    comments = [{"id": c.id, "content": c.content, "user": {"id": cu.id, "username": cu.username, "full_name": cu.full_name, "avatar_url": cu.avatar_url}, "created_at": c.created_at.isoformat()} for c, cu in r.all()]
    
    return {"id": p.id, "content": p.content, "images": p.images, "tags": p.tags, "user": {"id": u.id, "username": u.username, "full_name": u.full_name, "avatar_url": u.avatar_url, "is_premium": u.is_premium}, "likes_count": p.likes_count, "comments": comments, "comments_count": p.comments_count, "created_at": p.created_at.isoformat()}


@router.post("/{post_id}/like")
async def like_post(post_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Post, post_id)
    if not p: raise HTTPException(404)
    
    existing = await db.scalar(select(Like).where(Like.user_id == user.id, Like.target_type == "post", Like.target_id == post_id))
    if existing:
        await db.delete(existing)
        p.likes_count = max(0, p.likes_count - 1)
        await db.commit()
        return {"liked": False, "count": p.likes_count}
    
    db.add(Like(user_id=user.id, target_type="post", target_id=post_id))
    p.likes_count += 1
    
    if p.user_id != user.id:
        db.add(Notification(user_id=p.user_id, type=NotificationType.LIKE, title="Post yoqtirildi", message=f"{user.full_name} postigizni yoqtirdi", data={"post_id": post_id, "from_user_id": user.id}))
    
    await db.commit()
    return {"liked": True, "count": p.likes_count}


@router.post("/{post_id}/comments")
async def add_comment(post_id: int, req: CommentCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Post, post_id)
    if not p: raise HTTPException(404)
    
    c = Comment(post_id=post_id, user_id=user.id, content=req.content)
    db.add(c)
    p.comments_count += 1
    
    if p.user_id != user.id:
        db.add(Notification(user_id=p.user_id, type=NotificationType.COMMENT, title="Yangi izoh", message=f"{user.full_name} postigizga izoh qoldirdi", data={"post_id": post_id, "comment_id": c.id, "from_user_id": user.id}))
    
    await db.commit()
    return {"id": c.id, "content": c.content, "created_at": c.created_at.isoformat()}


@router.delete("/{post_id}")
async def delete_post(post_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Post, post_id)
    if not p or p.user_id != user.id: raise HTTPException(403)
    await db.delete(p)
    await db.commit()
    return {"message": "O'chirildi"}
