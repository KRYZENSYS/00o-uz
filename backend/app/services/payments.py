"""Payment service"""
from datetime import datetime, timedelta
from dataclasses import dataclass
from ..core.config import settings


@dataclass
class PaymentRequest:
    amount: float
    currency: str
    method: str
    user_id: int
    description: str = ""


async def process_payment(req: PaymentRequest) -> dict:
    if req.method == "payme": return await _payme(req)
    elif req.method == "click": return await _click(req)
    elif req.method == "uzum": return await _uzum(req)
    elif req.method == "stripe": return await _stripe(req)
    elif req.method == "ton": return await _ton(req)
    return {"error": "Unknown method"}


async def _payme(req): return {"method": "payme", "url": f"https://checkout.payme.uz/{settings.PAYME_MERCHANT_ID}/{req.amount}", "amount": req.amount, "status": "pending"}
async def _click(req): return {"method": "click", "url": f"https://my.click.uz/pay?amount={req.amount}", "amount": req.amount, "status": "pending"}
async def _uzum(req): return {"method": "uzum", "url": f"https://uzum.uz/pay?amount={req.amount}", "amount": req.amount, "status": "pending"}
async def _stripe(req): return {"method": "stripe", "url": f"https://checkout.stripe.com?amount={req.amount}", "amount": req.amount, "currency": "USD", "status": "pending"}
async def _ton(req): return {"method": "ton", "address": settings.TON_WALLET_ADDRESS, "amount": req.amount, "comment": f"user_{req.user_id}_{int(datetime.utcnow().timestamp())}", "status": "pending"}


async def activate_premium(user, days: int):
    user.is_premium = True
    user.premium_expires = datetime.utcnow() + timedelta(days=days)
    user.tokens += 1000
    return user
