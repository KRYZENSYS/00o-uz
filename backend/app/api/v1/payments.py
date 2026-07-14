"""Payments API"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.v1.auth import get_current_user
from app.models import User
from app.services.payments import process_payment, PaymentRequest

router = APIRouter(prefix="/payments", tags=["payments"])


class PayReq(BaseModel):
    amount: float
    currency: str = "UZS"
    method: str
    description: str = ""


@router.post("/create")
async def create(req: PayReq, user: User = Depends(get_current_user)):
    p = PaymentRequest(amount=req.amount, currency=req.currency, method=req.method, user_id=user.id, description=req.description)
    return await process_payment(p)


@router.get("/methods")
async def methods():
    return [
        {"id": "payme", "name": "Payme", "icon": "💳"},
        {"id": "click", "name": "Click", "icon": "📱"},
        {"id": "uzum", "name": "Uzum", "icon": "💰"},
        {"id": "stripe", "name": "Stripe (Card)", "icon": "💎"},
        {"id": "ton", "name": "TON", "icon": "💎"},
    ]


@router.get("/premium/plans")
async def plans():
    return [
        {"id": "month", "name": "1 oy", "price": 49000, "days": 30},
        {"id": "year", "name": "1 yil", "price": 490000, "days": 365},
        {"id": "lifetime", "name": "Umrbod", "price": 1999000, "days": 36500},
    ]
