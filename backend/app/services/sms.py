"""SMS Service - Eskiz.uz, Twilio"""
import os, httpx

ESKIZ_EMAIL = os.getenv("ESKIZ_EMAIL")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD")
ESKIZ_FROM = os.getenv("ESKIZ_FROM", "4546")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")


class EskizService:
    BASE_URL = "https://notify.eskiz.uz/api"

    @staticmethod
    async def get_token():
        async with httpx.AsyncClient() as c:
            r = await c.post(f"{EskizService.BASE_URL}/auth/login",
                json={"email": ESKIZ_EMAIL, "password": ESKIZ_PASSWORD})
            return r.json().get("data", {}).get("token")

    @staticmethod
    async def send_sms(phone: str, message: str):
        try:
            token = await EskizService.get_token()
            async with httpx.AsyncClient() as c:
                r = await c.post(f"{EskizService.BASE_URL}/message/sms/send",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"mobile_phone": phone.replace("+", ""), "message": message, "from": ESKIZ_FROM})
                return r.json()
        except Exception as e:
            return {"error": str(e)}


class TwilioService:
    @staticmethod
    async def send_sms(phone: str, message: str):
        from twilio.rest import Client
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            msg = client.messages.create(body=message, from_=TWILIO_FROM, to=phone)
            return {"sid": msg.sid, "status": msg.status}
        except Exception as e:
            return {"error": str(e)}


async def send_otp(phone: str, code: str):
    message = f"00o.uz tasdiqlash kodi: {code}"
    if phone.startswith("+998"):
        return await EskizService.send_sms(phone, message)
    return await TwilioService.send_sms(phone, message)
