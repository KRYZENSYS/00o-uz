"""Integrations, OAuth, Webhooks, Third-party"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import secrets, hmac, hashlib, json

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Integration, Webhook, WebhookDelivery, OAuthToken

router = APIRouter(prefix="/integrations", tags=["integrations"])


# Available integrations catalog
INTEGRATIONS = [
    {"id": "google_drive", "name": "Google Drive", "icon": "📁", "category": "storage", "desc": "Fayllarni Google Drive bilan sinxronlash", "color": "from-blue-500 to-green-500"},
    {"id": "dropbox", "name": "Dropbox", "icon": "📦", "category": "storage", "desc": "Dropbox bilan fayl almashish", "color": "from-blue-600 to-blue-800"},
    {"id": "github", "name": "GitHub", "icon": "🐙", "category": "dev", "desc": "GitHub repo va PR bilan ishlash", "color": "from-gray-700 to-gray-900"},
    {"id": "gitlab", "name": "GitLab", "icon": "🦊", "category": "dev", "desc": "GitLab bilan integratsiya", "color": "from-orange-500 to-red-600"},
    {"id": "slack", "name": "Slack", "icon": "💬", "category": "communication", "desc": "Slack kanalga xabar yuborish", "color": "from-purple-500 to-pink-600"},
    {"id": "discord", "name": "Discord", "icon": "🎮", "category": "communication", "desc": "Discord bilan integratsiya", "color": "from-indigo-500 to-purple-700"},
    {"id": "telegram", "name": "Telegram", "icon": "✈️", "category": "communication", "desc": "Telegram bot va kanal", "color": "from-blue-400 to-blue-600"},
    {"id": "notion", "name": "Notion", "icon": "📝", "category": "productivity", "desc": "Notion sahifalar bilan ishlash", "color": "from-gray-800 to-black"},
    {"id": "trello", "name": "Trello", "icon": "📋", "category": "productivity", "desc": "Trello board bilan sinxronlash", "color": "from-blue-400 to-cyan-500"},
    {"id": "asana", "name": "Asana", "icon": "✅", "category": "productivity", "desc": "Asana tasks bilan integratsiya", "color": "from-pink-500 to-red-500"},
    {"id": "jira", "name": "Jira", "icon": "🎯", "category": "productivity", "desc": "Jira issues bilan ishlash", "color": "from-blue-600 to-blue-800"},
    {"id": "linear", "name": "Linear", "icon": "📐", "category": "productivity", "desc": "Linear issues bilan integratsiya", "color": "from-purple-600 to-indigo-800"},
    {"id": "figma", "name": "Figma", "icon": "🎨", "category": "design", "desc": "Figma fayllar bilan ishlash", "color": "from-pink-500 to-orange-500"},
    {"id": "google_calendar", "name": "Google Calendar", "icon": "📅", "category": "productivity", "desc": "Kalendar bilan sinxronlash", "color": "from-blue-500 to-green-500"},
    {"id": "gmail", "name": "Gmail", "icon": "📧", "category": "communication", "desc": "Gmail bilan email yuborish", "color": "from-red-500 to-yellow-500"},
    {"id": "outlook", "name": "Outlook", "icon": "📨", "category": "communication", "desc": "Microsoft Outlook", "color": "from-blue-600 to-cyan-600"},
    {"id": "zoom", "name": "Zoom", "icon": "📹", "category": "communication", "desc": "Zoom meetings yaratish", "color": "from-blue-500 to-blue-700"},
    {"id": "google_meet", "name": "Google Meet", "icon": "🎥", "category": "communication", "desc": "Google Meet yaratish", "color": "from-green-500 to-blue-500"},
    {"id": "stripe", "name": "Stripe", "icon": "💳", "category": "payment", "desc": "Stripe to'lovlarni qabul qilish", "color": "from-purple-600 to-indigo-600"},
    {"id": "mailchimp", "name": "Mailchimp", "icon": "🐵", "category": "marketing", "desc": "Email marketing", "color": "from-yellow-400 to-orange-500"},
    {"id": "sendgrid", "name": "SendGrid", "icon": "📬", "category": "communication", "desc": "Email xizmati", "color": "from-blue-500 to-cyan-600"},
    {"id": "twilio", "name": "Twilio", "icon": "📱", "category": "communication", "desc": "SMS yuborish", "color": "from-red-500 to-pink-500"},
    {"id": "sentry", "name": "Sentry", "icon": "🚨", "category": "dev", "desc": "Error monitoring", "color": "from-purple-700 to-pink-700"},
    {"id": "google_analytics", "name": "Google Analytics", "icon": "📊", "category": "analytics", "desc": "Veb-analitika", "color": "from-orange-500 to-yellow-500"},
    {"id": "mixpanel", "name": "Mixpanel", "icon": "📈", "category": "analytics", "desc": "Product analytics", "color": "from-purple-500 to-blue-600"},
    {"id": "hubspot", "name": "HubSpot", "icon": "🟠", "category": "marketing", "desc": "CRM va marketing", "color": "from-orange-500 to-red-500"},
    {"id": "salesforce", "name": "Salesforce", "icon": "☁️", "category": "sales", "desc": "CRM platforma", "color": "from-blue-400 to-cyan-500"},
    {"id": "zapier", "name": "Zapier", "icon": "⚡", "category": "automation", "desc": "Workflow automation", "color": "from-orange-500 to-red-600"},
    {"id": "make", "name": "Make (Integromat)", "icon": "🔧", "category": "automation", "desc": "No-code automation", "color": "from-purple-600 to-pink-600"},
    {"id": "airtable", "name": "Airtable", "icon": "📊", "category": "productivity", "desc": "Database va spreadsheets", "color": "from-yellow-500 to-orange-500"},
    {"id": "google_sheets", "name": "Google Sheets", "icon": "📑", "category": "productivity", "desc": "Google Sheets bilan ishlash", "color": "from-green-500 to-emerald-600"},
    {"id": "twitter", "name": "Twitter / X", "icon": "🐦", "category": "social", "desc": "Twitter post va analytics", "color": "from-blue-400 to-black"},
    {"id": "linkedin", "name": "LinkedIn", "icon": "💼", "category": "social", "desc": "LinkedIn post va messaging", "color": "from-blue-600 to-blue-800"},
    {"id": "youtube", "name": "YouTube", "icon": "📺", "category": "social", "desc": "YouTube video yuklash", "color": "from-red-500 to-red-700"},
    {"id": "instagram", "name": "Instagram", "icon": "📸", "category": "social", "desc": "Instagram post va stories", "color": "from-pink-500 via-purple-500 to-orange-500"},
    {"id": "tiktok", "name": "TikTok", "icon": "🎵", "category": "social", "desc": "TikTok video yuklash", "color": "from-black to-pink-600"},
    {"id": "facebook", "name": "Facebook", "icon": "👥", "category": "social", "desc": "Facebook pages", "color": "from-blue-500 to-blue-700"},
    {"id": "pinterest", "name": "Pinterest", "icon": "📌", "category": "social", "desc": "Pinterest pins", "color": "from-red-500 to-rose-600"},
    {"id": "vk", "name": "VK", "icon": "🇷🇺", "category": "social", "desc": "VKontakte", "color": "from-blue-500 to-blue-700"},
    {"id": "telegram_bots", "name": "Telegram Bot API", "icon": "🤖", "category": "dev", "desc": "Bots yaratish", "color": "from-blue-400 to-cyan-500"},
]


@router.get("/catalog")
async def catalog(category: Optional[str] = None):
    """List all available integrations"""
    if category:
        return [i for i in INTEGRATIONS if i["category"] == category]
    return INTEGRATIONS


@router.get("/my")
async def my_integrations(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Integration).where(Integration.user_id == user.id))
    return [{"id": i.id, "service": i.service, "account_name": i.account_name, "is_active": i.is_active, "connected_at": i.connected_at.isoformat()} for i in r.scalars().all()]


@router.post("/connect/{service}")
async def connect(service: str, account_name: str = "default", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Initiate OAuth flow for a service"""
    valid = [i["id"] for i in INTEGRATIONS]
    if service not in valid: raise HTTPException(400, "Service topilmadi")
    
    # Generate OAuth state
    state = secrets.token_urlsafe(32)
    
    # Check existing
    existing = await db.scalar(select(Integration).where(Integration.user_id == user.id, Integration.service == service, Integration.account_name == account_name))
    if existing:
        existing.is_active = True
        await db.commit()
        return {"id": existing.id, "message": "Qayta ulandi", "auth_url": f"https://oauth.00o.uz/{service}?state={state}"}
    
    integration = Integration(user_id=user.id, service=service, account_name=account_name, is_active=True, connected_at=datetime.utcnow())
    db.add(integration); await db.commit()
    
    return {"id": integration.id, "auth_url": f"https://oauth.00o.uz/{service}?state={state}"}


@router.post("/disconnect/{integration_id}")
async def disconnect(integration_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    i = await db.get(Integration, integration_id)
    if not i or i.user_id != user.id: raise HTTPException(404)
    i.is_active = False
    await db.commit()
    return {"message": "Uzildi"}


# ============ WEBHOOKS ============
class WebhookReq(BaseModel):
    url: str
    events: List[str]  # ["user.created", "order.paid", "post.liked"]
    secret: Optional[str] = None
    is_active: bool = True


@router.post("/webhooks")
async def create_webhook(req: WebhookReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = req.secret or secrets.token_urlsafe(32)
    w = Webhook(user_id=user.id, **req.dict(), secret=secret)
    db.add(w); await db.commit(); await db.refresh(w)
    return {"id": w.id, "url": w.url, "secret": w.secret, "events": w.events}


@router.get("/webhooks")
async def list_webhooks(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Webhook).where(Webhook.user_id == user.id))
    return [{"id": w.id, "url": w.url, "events": w.events, "is_active": w.is_active, "created_at": w.created_at.isoformat()} for w in r.scalars().all()]


@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    w = await db.get(Webhook, webhook_id)
    if not w or w.user_id != user.id: raise HTTPException(404)
    await db.delete(w); await db.commit()
    return {"message": "O'chirildi"}


@router.get("/webhooks/{webhook_id}/deliveries")
async def webhook_deliveries(webhook_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(WebhookDelivery).where(WebhookDelivery.webhook_id == webhook_id).order_by(WebhookDelivery.created_at.desc()).limit(50))
    return [{"id": d.id, "event": d.event, "status": d.status, "response_code": d.response_code, "created_at": d.created_at.isoformat()} for d in r.scalars().all()]


# ============ API KEYS (for external integrations) ============
class APIKeyReq(BaseModel):
    name: str
    scopes: List[str] = ["read"]


@router.post("/api-keys")
async def create_api_key(req: APIKeyReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import APIKey
    key = f"oo0o_live_{secrets.token_urlsafe(32)}"
    ak = APIKey(user_id=user.id, name=req.name, key_hash=hashlib.sha256(key.encode()).hexdigest(), scopes=req.scopes, prefix=key[:20])
    db.add(ak); await db.commit()
    return {"key": key, "warning": "Bu kalitni xavfsiz saqlang. Qayta ko'rsatilmaydi!"}


@router.get("/api-keys")
async def list_api_keys(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import APIKey
    r = await db.execute(select(APIKey).where(APIKey.user_id == user.id))
    return [{"id": k.id, "name": k.name, "prefix": k.prefix, "scopes": k.scopes, "last_used": k.last_used.isoformat() if k.last_used else None, "created_at": k.created_at.isoformat()} for k in r.scalars().all()]


@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models import APIKey
    k = await db.get(APIKey, key_id)
    if not k or k.user_id != user.id: raise HTTPException(404)
    await db.delete(k); await db.commit()
    return {"message": "O'chirildi"}


# ============ WEBHOOK TRIGGER (internal) ============
async def trigger_webhooks(db: AsyncSession, user_id: int, event: str, payload: dict):
    """Internal helper to trigger user webhooks"""
    r = await db.execute(select(Webhook).where(Webhook.user_id == user_id, Webhook.is_active == True))
    import aiohttp
    async with aiohttp.ClientSession() as session:
        for w in r.scalars().all():
            if event in w.events or "*" in w.events:
                signature = hmac.new(w.secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()
                headers = {"X-00o-Signature": signature, "X-00o-Event": event, "Content-Type": "application/json"}
                try:
                    async with session.post(w.url, json=payload, headers=headers, timeout=10) as resp:
                        delivery = WebhookDelivery(webhook_id=w.id, event=event, payload=payload, response_code=resp.status, status="success" if resp.status < 400 else "failed")
                        db.add(delivery)
                except Exception as e:
                    delivery = WebhookDelivery(webhook_id=w.id, event=event, payload=payload, response_code=0, status="failed", error=str(e))
                    db.add(delivery)
        await db.commit()
