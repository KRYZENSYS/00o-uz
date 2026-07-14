"""Email service"""
import httpx
from ..core.config import settings


class EmailService:
    @staticmethod
    async def send(to: str, subject: str, html: str) -> bool:
        if not settings.SENDGRID_API_KEY: return False
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}", "Content-Type": "application/json"},
                    json={"personalizations": [{"to": [{"email": to}]}], "from": {"email": settings.EMAIL_FROM, "name": "00o.uz"},
                          "subject": subject, "content": [{"type": "text/html", "value": html}]}
                )
            return True
        except: return False

    @staticmethod
    async def send_welcome(email: str, name: str):
        return await EmailService.send(email, "00o.uz ga xush kelibsiz! 🎉",
            f"<h1>Salom, {name}!</h1><p>00o.uz ga qo'shilganingizdan xursandmiz!</p>")

    @staticmethod
    async def send_password_reset(email: str, link: str):
        return await EmailService.send(email, "Parolni tiklash", f"<h1>Parolni tiklash</h1><p><a href='{link}'>Bu yerni bosing</a> yangi parol o'rnatish uchun.</p>")

    @staticmethod
    async def send_premium_activated(email: str, name: str, plan: str):
        return await EmailService.send(email, f"💎 Premium faollashtirildi - {plan}",
            f"<h1>Tabriklaymiz, {name}!</h1><p>Premium {plan} faollashtirildi!</p>")
