"""Investors API - investor profiles, deals"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Investor, InvestorType, Deal, DealStatus

router = APIRouter(prefix="/investors", tags=["investors"])


class InvestorCreate(BaseModel):
    name: str
    type: str  # angel, vc, fund, accelerator
    bio: str
    min_investment: float
    max_investment: float
    currency: str = "USD"
    industries: List[str] = []
    stages: List[str] = []
    location: Optional[str] = None
    website: Optional[str] = None
    portfolio_count: int = 0


class DealCreate(BaseModel):
    startup_id: int
    amount: float
    equity: float
    valuation: float
    message: str = ""


@router.get("/")
async def list_investors(search: Optional[str] = None, type: Optional[str] = None, industry: Optional[str] = None, limit: int = Query(50, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Investor).where(Investor.is_active == True)
    if search: q = q.where(or_(Investor.name.ilike(f"%{search}%"), Investor.bio.ilike(f"%{search}%")))
    if type: q = q.where(Investor.type == type)
    q = q.order_by(Investor.is_featured.desc(), Investor.total_invested.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": i.id, "name": i.name, "type": i.type.value, "bio": i.bio, "min_investment": i.min_investment, "max_investment": i.max_investment, "currency": i.currency, "industries": i.industries, "stages": i.stages, "location": i.location, "website": i.website, "portfolio_count": i.portfolio_count, "total_invested": i.total_invested, "is_verified": i.is_verified, "is_featured": i.is_featured} for i in r.scalars().all()]


@router.get("/{investor_id}")
async def get_investor(investor_id: int, db: AsyncSession = Depends(get_db)):
    i = await db.get(Investor, investor_id)
    if not i: raise HTTPException(404)
    return {"id": i.id, "name": i.name, "type": i.type.value, "bio": i.bio, "min_investment": i.min_investment, "max_investment": i.max_investment, "currency": i.currency, "industries": i.industries, "stages": i.stages, "location": i.location, "website": i.website, "portfolio_count": i.portfolio_count, "total_invested": i.total_invested, "is_verified": i.is_verified}


@router.post("/")
async def create_investor(req: InvestorCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    i = Investor(user_id=user.id, name=req.name, type=InvestorType(req.type), bio=req.bio, min_investment=req.min_investment, max_investment=req.max_investment, currency=req.currency, industries=req.industries, stages=req.stages, location=req.location, website=req.website, portfolio_count=req.portfolio_count)
    db.add(i)
    await db.commit()
    return {"id": i.id}


@router.post("/deals")
async def create_deal(req: DealCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = Deal(startup_id=req.startup_id, investor_id=user.id, amount=req.amount, equity=req.equity, valuation=req.valuation, message=req.message, status=DealStatus.PENDING)
    db.add(d)
    await db.commit()
    return {"id": d.id, "status": d.status.value}


@router.get("/deals/my")
async def my_deals(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Deal).where(Deal.investor_id == user.id).order_by(Deal.created_at.desc()))
    return [{"id": d.id, "startup_id": d.startup_id, "amount": d.amount, "equity": d.equity, "status": d.status.value, "created_at": d.created_at.isoformat()} for d in r.scalars().all()]


@router.post("/deals/{deal_id}/accept")
async def accept_deal(deal_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = await db.get(Deal, deal_id)
    if not d: raise HTTPException(404)
    # Verify user is the startup owner
    from app.models import Startup
    s = await db.get(Startup, d.startup_id)
    if not s or s.owner_id != user.id: raise HTTPException(403)
    d.status = DealStatus.ACCEPTED
    s.funding_raised += d.amount
    await db.commit()
    return {"message": "Qabul qilindi"}


@router.post("/deals/{deal_id}/reject")
async def reject_deal(deal_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = await db.get(Deal, deal_id)
    if not d: raise HTTPException(404)
    from app.models import Startup
    s = await db.get(Startup, d.startup_id)
    if not s or s.owner_id != user.id: raise HTTPException(403)
    d.status = DealStatus.REJECTED
    await db.commit()
    return {"message": "Rad etildi"}
