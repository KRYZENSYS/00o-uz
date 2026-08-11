"""
GitHub API service - public read-only access, no auth needed for basic queries.
Uses GitHub REST API directly.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

GH_API = "https://api.github.com"
CACHE: Dict[str, Dict[str, Any]] = {}


def _gh_headers() -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    return headers


async def gh_user(username: str) -> Dict[str, Any]:
    username = (username or "").strip().lower()
    if not username:
        return {"error": "Empty username"}
    cache_key = f"user:{username}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{GH_API}/users/{username}", headers=_gh_headers())
            if r.status_code == 404:
                return {"error": "User not found"}
            data = r.json()
            CACHE[cache_key] = data
            return data
    except Exception as e:
        return {"error": str(e)}


async def gh_repos(username: str, limit: int = 20, sort: str = "updated") -> List[Dict[str, Any]]:
    username = (username or "").strip().lower()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{GH_API}/users/{username}/repos",
                params={"per_page": min(limit, 100), "sort": sort, "type": "owner"},
                headers=_gh_headers(),
            )
            if r.status_code == 404:
                return []
            return r.json()
    except Exception as e:
        logger.error("gh_repos error: %s", e)
        return []


async def gh_search_repos(q: str, limit: int = 20) -> List[Dict[str, Any]]:
    q = (q or "").strip()
    if not q:
        return []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{GH_API}/search/repositories",
                                 params={"q": q, "per_page": min(limit, 100), "sort": "stars"},
                                 headers=_gh_headers())
            if r.status_code != 200:
                return []
            return r.json().get("items", [])
    except Exception as e:
        return []


async def gh_trending(since: str = "daily", language: Optional[str] = None) -> List[Dict[str, Any]]:
    days_map = {"daily": 1, "weekly": 7, "monthly": 30}
    days = days_map.get(since, 7)
    date_str = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"created:>{date_str}"
    if language:
        q += f" language:{language}"
    return await gh_search_repos(q, limit=20)
