"""Configuration"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "00o.uz"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this"
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/00o_uz"
    REDIS_URL: str = "redis://localhost:6379"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    OPENAI_API_KEY: str = ""

    TELEGRAM_BOT_TOKEN: str = ""
    WEBAPP_URL: str = "https://00o.uz"
    API_URL: str = "http://localhost:8000"

    SENDGRID_API_KEY: str = ""
    EMAIL_FROM: str = "info@00o.uz"

    ESKIZ_EMAIL: str = ""
    ESKIZ_PASSWORD: str = ""

    PAYME_MERCHANT_ID: str = ""
    PAYME_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    TON_WALLET_ADDRESS: str = ""

    SENTRY_DSN: str = ""
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
