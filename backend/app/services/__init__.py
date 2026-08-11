"""Services init."""
from app.services import (
    ip_service,
    dns_service,
    whois_service,
    translate_service,
    weather_service,
    news_service,
    currency_service,
    github_service,
    download_service,
)

__all__ = [
    "ip_service",
    "dns_service",
    "whois_service",
    "translate_service",
    "weather_service",
    "news_service",
    "currency_service",
    "github_service",
    "download_service",
]
