"""Email Service - SendGrid"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@00o.uz")


class EmailService:
    client = SendGridAPIClient(SENDGRID_API_KEY) if SENDGRID_API_KEY else None

    @staticmethod
    async def send(to: str, subject: str, html: str, text: str = None):
        if not EmailService.client:
            return {"error": "Not configured"}
        message = Mail(from_email=Email(FROM_EMAIL), to_emails=To(to), subject=subject,
                       html_content=Content("text/html", html))
        try:
            response = EmailService.client.send(message)
            return {"status": "sent", "code": response.status_code}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    async def send_verification(to: str, code: str):
        await EmailService.send(to, "Email tasdiqlash", f"<h1>Kod: {code}</h1>", f"Kod: {code}")

    @staticmethod
    async def send_welcome(to: str, name: str):
        await EmailService.send(to, "Xush kelibsiz!", f"<h1>Salom, {name}!</h1>")

    @staticmethod
    async def send_premium_activated(to: str, days: int):
        await EmailService.send(to, "Premium faollashtirildi", f"<h1>💎 {days} kunlik premium</h1>")
