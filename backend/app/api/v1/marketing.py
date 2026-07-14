"""Marketing tools, Blog, Newsletter, Coupons, Email marketing"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import secrets

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, BlogPost, BlogComment, Newsletter, Subscriber, Coupon, CouponUsage, EmailCampaign, PushNotification, Landing

router = APIRouter(prefix="/marketing", tags=["marketing"])


# ==================== BLOG ====================
class BlogPostReq(BaseModel):
    title: str
    slug: Optional[str] = None
    content: str
    excerpt: str
    cover_image: Optional[str] = None
    category: str = "general"
    tags: Optional[List[str]] = []
    is_published: bool = False


@router.post("/blog/posts")
async def create_blog_post(req: BlogPostReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    slug = req.slug or req.title.lower().replace(" ", "-")[:80]
    p = BlogPost(author_id=user.id, **req.dict(), slug=slug, published_at=datetime.utcnow() if req.is_published else None)
    db.add(p); await db.commit(); await db.refresh(p)
    return {"id": p.id, "slug": p.slug}


@router.get("/blog/posts")
async def list_blog_posts(category: Optional[str] = None, search: Optional[str] = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(BlogPost).where(BlogPost.is_published == True)
    if category: q = q.where(BlogPost.category == category)
    if search: q = q.where(BlogPost.title.ilike(f"%{search}%"))
    q = q.order_by(BlogPost.published_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": p.id, "title": p.title, "slug": p.slug, "excerpt": p.excerpt, "cover_image": p.cover_image, "category": p.category, "author": p.author.full_name if p.author else None, "views_count": p.views_count, "likes_count": p.likes_count, "published_at": p.published_at.isoformat() if p.published_at else None} for p in r.scalars().all()]


@router.get("/blog/posts/{slug}")
async def get_blog_post(slug: str, db: AsyncSession = Depends(get_db)):
    p = await db.scalar(select(BlogPost).where(BlogPost.slug == slug))
    if not p: raise HTTPException(404)
    p.views_count += 1
    await db.commit()
    return {"id": p.id, "title": p.title, "content": p.content, "excerpt": p.excerpt, "cover_image": p.cover_image, "category": p.category, "tags": p.tags, "author": {"id": p.author.id, "full_name": p.author.full_name, "avatar_url": p.author.avatar_url}, "views_count": p.views_count, "likes_count": p.likes_count, "published_at": p.published_at.isoformat() if p.published_at else None}


@router.post("/blog/posts/{post_id}/like")
async def like_post(post_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(BlogPost, post_id)
    if not p: raise HTTPException(404)
    p.likes_count += 1
    await db.commit()
    return {"likes": p.likes_count}


@router.post("/blog/posts/{post_id}/comment")
async def comment_post(post_id: int, content: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = BlogComment(post_id=post_id, user_id=user.id, content=content)
    db.add(c); await db.commit()
    return {"id": c.id}


# ==================== NEWSLETTER ====================
@router.post("/newsletter/subscribe")
async def subscribe(email: EmailStr, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(Subscriber).where(Subscriber.email == email))
    if existing:
        existing.is_active = True
        await db.commit()
        return {"message": "Allaqachon obuna bo'lgansiz"}
    sub = Subscriber(email=email, confirm_token=secrets.token_urlsafe(16))
    db.add(sub); await db.commit()
    return {"message": "Obuna bo'ldingiz!", "token": sub.confirm_token}


@router.post("/newsletter/unsubscribe")
async def unsubscribe(token: str, db: AsyncSession = Depends(get_db)):
    sub = await db.scalar(select(Subscriber).where(Subscriber.confirm_token == token))
    if sub:
        sub.is_active = False
        await db.commit()
    return {"message": "Obuna bekor qilindi"}


# ==================== COUPONS ====================
class CouponReq(BaseModel):
    code: str
    discount_type: str = "percent"  # percent, fixed
    discount_value: float
    max_uses: Optional[int] = None
    min_order: float = 0
    expires_at: Optional[datetime] = None
    applicable_to: Optional[str] = None  # market, courses, services


@router.post("/coupons")
async def create_coupon(req: CouponReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ["admin", "moderator"]: raise HTTPException(403)
    c = Coupon(**req.dict(), created_by=user.id)
    db.add(c); await db.commit(); await db.refresh(c)
    return {"id": c.id, "code": c.code}


@router.post("/coupons/apply")
async def apply_coupon(code: str, order_total: float, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.scalar(select(Coupon).where(Coupon.code == code, Coupon.is_active == True))
    if not c: raise HTTPException(404, "Coupon topilmadi")
    if c.expires_at and c.expires_at < datetime.utcnow(): raise HTTPException(400, "Coupon eskirgan")
    if c.max_uses and c.uses_count >= c.max_uses: raise HTTPException(400, "Coupon limiti tugagan")
    if order_total < c.min_order: raise HTTPException(400, f"Minimal buyurtma: {c.min_order}")
    
    used = await db.scalar(select(CouponUsage).where(CouponUsage.coupon_id == c.id, CouponUsage.user_id == user.id))
    if used: raise HTTPException(400, "Allaqachon ishlatilgan")
    
    if c.discount_type == "percent": discount = order_total * c.discount_value / 100
    else: discount = c.discount_value
    
    db.add(CouponUsage(coupon_id=c.id, user_id=user.id, discount=discount))
    c.uses_count += 1
    await db.commit()
    return {"discount": discount, "new_total": order_total - discount}


# ==================== EMAIL CAMPAIGNS ====================
class CampaignReq(BaseModel):
    name: str
    subject: str
    content: str
    segment: Optional[str] = "all"  # all, premium, free, active
    scheduled_at: Optional[datetime] = None


@router.post("/campaigns")
async def create_campaign(req: CampaignReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ["admin", "moderator"]: raise HTTPException(403)
    c = EmailCampaign(**req.dict(), created_by=user.id, status="draft")
    db.add(c); await db.commit(); await db.refresh(c)
    return {"id": c.id}


@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(campaign_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ["admin", "moderator"]: raise HTTPException(403)
    c = await db.get(EmailCampaign, campaign_id)
    if not c: raise HTTPException(404)
    c.status = "sent"
    c.sent_at = datetime.utcnow()
    await db.commit()
    return {"message": "Yuborildi"}


# ==================== PUSH NOTIFICATIONS ====================
class PushReq(BaseModel):
    title: str
    body: str
    icon: Optional[str] = None
    url: Optional[str] = None
    target_users: Optional[str] = "all"  # all, premium, online
    data: Optional[dict] = None


@router.post("/push/send")
async def send_push(req: PushReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ["admin", "moderator"]: raise HTTPException(403)
    p = PushNotification(**req.dict(), sent_by=user.id, sent_at=datetime.utcnow())
    db.add(p); await db.commit()
    return {"id": p.id, "message": "Yuborildi"}


@router.get("/push/my")
async def my_pushes(limit: int = 20, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(PushNotification).where(PushNotification.target_users == "all").order_by(PushNotification.sent_at.desc()).limit(limit))
    return [{"id": p.id, "title": p.title, "body": p.body, "icon": p.icon, "url": p.url, "sent_at": p.sent_at.isoformat()} for p in r.scalars().all()]


# ==================== LANDING PAGES ====================
class LandingReq(BaseModel):
    name: str
    title: str
    description: str
    hero_image: Optional[str] = None
    content: str  # HTML or JSON blocks
    cta_text: str = "Boshlash"
    cta_url: str = "/register"
    theme: str = "default"


@router.post("/landings")
async def create_landing(req: LandingReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    l = Landing(owner_id=user.id, **req.dict(), slug=req.name.lower().replace(" ", "-"))
    db.add(l); await db.commit(); await db.refresh(l)
    return {"id": l.id, "slug": l.slug, "url": f"/l/{l.slug}"}


@router.get("/landings/{slug}")
async def get_landing(slug: str, db: AsyncSession = Depends(get_db)):
    l = await db.scalar(select(Landing).where(Landing.slug == slug, Landing.is_published == True))
    if not l: raise HTTPException(404)
    l.views_count += 1
    await db.commit()
    return {"name": l.name, "title": l.title, "description": l.description, "hero_image": l.hero_image, "content": l.content, "cta_text": l.cta_text, "cta_url": l.cta_url, "theme": l.theme}


# ==================== SEO ====================
@router.get("/seo/sitemap.xml")
async def sitemap(db: AsyncSession = Depends(get_db)):
    """Generate XML sitemap"""
    r = await db.execute(select(BlogPost).where(BlogPost.is_published == True).limit(1000))
    posts = r.scalars().all()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in posts:
        xml += f"<url><loc>https://00o.uz/blog/{p.slug}</loc><lastmod>{p.updated_at.date()}</lastmod></url>\n"
    xml += "</urlset>"
    return {"content": xml, "content_type": "application/xml"}


@router.get("/seo/robots.txt")
async def robots():
    return {"content": "User-agent: *\nAllow: /\nSitemap: https://00o.uz/sitemap.xml", "content_type": "text/plain"}


# ==================== ANALYTICS ====================
@router.post("/analytics/event")
async def track_event(event_name: str, properties: Optional[dict] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Track custom analytics event"""
    # In production: save to analytics table or external service
    return {"tracked": True, "event": event_name, "user_id": user.id}


@router.get("/analytics/overview")
async def analytics_overview(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import User
    total_users = await db.scalar(select(func.count(User.id))) or 0
    new_today = await db.scalar(select(func.count(User.id)).where(func.date(User.created_at) == datetime.utcnow().date())) or 0
    return {"total_users": total_users, "new_today": new_today, "active_users": total_users, "your_views": 0}
