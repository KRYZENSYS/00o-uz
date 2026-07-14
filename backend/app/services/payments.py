"""Payment Services - Payme, Click, Uzum, Stripe, TON"""
import os, json, hmac, hashlib, time
from pydantic import BaseModel

PAYME_SECRET = os.getenv("PAYME_SECRET")
CLICK_SECRET = os.getenv("CLICK_SECRET")
UZUM_SECRET = os.getenv("UZUM_SECRET")

import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentRequest(BaseModel):
    amount: float
    currency: str = "UZS"
    method: str
    user_id: int
    description: str = ""


class PaymeService:
    @staticmethod
    def create_transaction(order_id: str, amount: int) -> dict:
        return {
            "method": "cards.create",
            "params": {"card": {"number": "", "expire": ""}, "amount": amount, "account": {"order_id": order_id}}
        }


class ClickService:
    @staticmethod
    def create_invoice(amount: float, order_id: str, phone: str) -> dict:
        return {"service_id": os.getenv("CLICK_SERVICE_ID"), "amount": amount,
                "phone_number": phone, "merchant_trans_id": order_id}


class UzumService:
    @staticmethod
    def create_payment(amount: float, order_id: str, phone: str) -> dict:
        return {"merchant_id": os.getenv("UZUM_MERCHANT_ID"), "amount": amount,
                "phone": phone, "order_id": order_id}


class StripeService:
    @staticmethod
    def create_checkout(amount: float, currency: str, success_url: str, cancel_url: str):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{"price_data": {"currency": currency.lower(),
                              "product_data": {"name": "00o.uz Premium"},
                              "unit_amount": int(amount * 100)}, "quantity": 1}],
                mode="payment", success_url=success_url, cancel_url=cancel_url,
            )
            return {"url": session.url, "session_id": session.id}
        except Exception as e:
            return {"error": str(e)}


class TONService:
    @staticmethod
    async def create_ton_payment(wallet_address: str, amount: float, comment: str):
        ton_amount = amount / 30000
        return {"wallet": wallet_address, "amount": ton_amount, "comment": comment,
                "ton_url": f"ton://transfer/{wallet_address}?amount={int(ton_amount * 1e9)}&text={comment}"}


async def process_payment(req: PaymentRequest) -> dict:
    order_id = f"order_{req.user_id}_{int(time.time())}"
    if req.method == "payme":
        return PaymeService.create_transaction(order_id, int(req.amount * 100))
    elif req.method == "click":
        return ClickService.create_invoice(req.amount, order_id, "+998901234567")
    elif req.method == "uzum":
        return UzumService.create_payment(req.amount, order_id, "+998901234567")
    elif req.method == "stripe":
        return StripeService.create_checkout(req.amount, req.currency, "https://00o.uz/success", "https://00o.uz/cancel")
    elif req.method == "ton":
        return await TONService.create_ton_payment("UQB...00o", req.amount, order_id)
    return {"error": "Unknown method"}
