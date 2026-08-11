"""
Real API tools endpoints: IP, DNS, WHOIS, translate, weather, news, currency, github, download.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Any, Dict, List, Optional

from app.services.ip_service import get_ip_info
from app.services.dns_service import dns_lookup, bulk_dns
from app.services.whois_service import whois_lookup
from app.services.translate_service import translate, detect_language
from app.services.weather_service import get_weather, geocode, weather_code_to_text
from app.services.news_service import get_hackernews, get_reddit, get_rss_feed, get_aggregated_news
from app.services.currency_service import get_currencies, get_rate, get_crypto, get_timeseries
from app.services.github_service import gh_user, gh_repos, gh_search_repos, gh_trending
from app.services.download_service import download_media, get_video_info, PLATFORMS

router = APIRouter(prefix="/api/v1/tools", tags=["tools"])


@router.get("/ip")
async def tool_ip(request: Request, ip: Optional[str] = None) -> Dict[str, Any]:
    """Get geolocation for current IP (or specified)."""
    target = ip or (request.client.host if request.client else None)
    return await get_ip_info(target)


@router.get("/dns")
async def tool_dns(
    domain: str = Query(..., min_length=1),
    type: str = Query("A", description="A, AAAA, MX, TXT, NS, CNAME, SOA, PTR, SRV"),
) -> Dict[str, Any]:
    """DNS lookup for a domain."""
    return await dns_lookup(domain, type)


@router.get("/dns/bulk")
async def tool_dns_bulk(domain: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Bulk DNS lookup: A, AAAA, MX, TXT, NS, CNAME."""
    return await bulk_dns(domain)


@router.get("/whois")
async def tool_whois(domain: str = Query(..., min_length=3)) -> Dict[str, Any]:
    """WHOIS/RDAP lookup for a domain."""
    return await whois_lookup(domain)


@router.get("/translate")
async def tool_translate(
    text: str = Query(..., min_length=1, max_length=500),
    target: str = Query("en", max_length=5),
    source: Optional[str] = None,
) -> Dict[str, Any]:
    """Translate text to target language (MyMemory)."""
    return await translate(text, target, source)


@router.get("/detect")
async def tool_detect(text: str = Query(..., min_length=1, max_length=500)) -> Dict[str, Any]:
    """Detect language of text."""
    return await detect_language(text)


@router.get("/weather")
async def tool_weather(city: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Get current weather + 7-day forecast for a city."""
    data = await get_weather(city)
    if "current" in data and data["current"].get("weather_code") is not None:
        wc = weather_code_to_text(data["current"]["weather_code"])
        data["current"]["text"] = wc["text"]
        data["current"]["emoji"] = wc["emoji"]
    return data


@router.get("/geocode")
async def tool_geocode(city: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Geocode a city to lat/lon."""
    return await geocode(city)


@router.get("/news/hackernews")
async def tool_hn(limit: int = Query(20, ge=1, le=50)) -> List[Dict[str, Any]]:
    """Top stories from Hacker News."""
    return await get_hackernews(limit)


@router.get("/news/reddit")
async def tool_reddit(subreddit: str = "technology", limit: int = Query(25, ge=1, le=100)) -> List[Dict[str, Any]]:
    """Top posts from a subreddit."""
    return await get_reddit(subreddit, limit)


@router.get("/news/rss")
async def tool_rss(url: str = Query(...), limit: int = Query(15, ge=1, le=50)) -> List[Dict[str, Any]]:
    """Parse an RSS feed."""
    return await get_rss_feed(url, limit)


@router.get("/news")
async def tool_news(q: Optional[str] = None) -> Dict[str, Any]:
    """Aggregated news from HN + Reddit + RSS."""
    return await get_aggregated_news(q)


@router.get("/currency/list")
async def tool_currency_list() -> Dict[str, str]:
    """All supported fiat currencies."""
    return await get_currencies()


@router.get("/currency/rate")
async def tool_currency_rate(
    base: str = "USD",
    target: str = "EUR",
    amount: float = 1.0,
) -> Dict[str, Any]:
    """Convert currency."""
    return await get_rate(base, target, amount)


@router.get("/currency/crypto")
async def tool_currency_crypto(
    ids: str = "bitcoin,ethereum,solana,toncoin,binancecoin",
    vs: str = "usd",
) -> Dict[str, Any]:
    """Get crypto prices (CoinGecko)."""
    return await get_crypto(ids.split(","), vs)


@router.get("/currency/timeseries")
async def tool_currency_timeseries(
    base: str = "USD",
    target: str = "UZS",
    days: int = Query(30, ge=1, le=365),
) -> Dict[str, Any]:
    """Historical rates."""
    return await get_timeseries(base, target, days)


@router.get("/github/user")
async def tool_gh_user(username: str = Query(..., min_length=1)) -> Dict[str, Any]:
    """Get GitHub user profile."""
    return await gh_user(username)


@router.get("/github/repos")
async def tool_gh_repos(
    username: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = "updated",
) -> List[Dict[str, Any]]:
    """Get user's public repos."""
    return await gh_repos(username, limit, sort)


@router.get("/github/search")
async def tool_gh_search(q: str = Query(..., min_length=2), limit: int = Query(20, ge=1, le=100)) -> List[Dict[str, Any]]:
    """Search GitHub repositories."""
    return await gh_search_repos(q, limit)


@router.get("/github/trending")
async def tool_gh_trending(
    since: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Trending repositories (approximated by stars in last N days)."""
    return await gh_trending(since, language)


@router.get("/download/info")
async def tool_download_info(url: str = Query(...)) -> Dict[str, Any]:
    """Get video metadata (no download)."""
    return await get_video_info(url)


@router.post("/download")
async def tool_download(
    url: str = Query(...),
    format: str = "mp4",
    quality: str = "best",
) -> Dict[str, Any]:
    """Download media from YouTube/TikTok/Instagram/Twitter via yt-dlp."""
    return await download_media(url, format, quality)


@router.get("/download/platforms")
async def tool_download_platforms() -> Dict[str, Any]:
    """List supported platforms."""
    return {"platforms": PLATFORMS, "count": len(PLATFORMS)}
