"""
News service - aggregates free sources: HackerNews, Reddit, RSS feeds.
"""

import asyncio
import logging
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
REDDIT_RSS = "https://www.reddit.com/r/{subreddit}/.rss?limit=25"
RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://techcrunch.com/feed/",
]

CACHE: Dict[str, Dict[str, Any]] = {}


async def get_hackernews(limit: int = 20) -> List[Dict[str, Any]]:
    cache_key = f"hn:{limit}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(HN_TOP)
            ids = r.json()[:limit]
            results = []
            for story_id in ids:
                try:
                    item_r = await client.get(HN_ITEM.format(id=story_id))
                    item = item_r.json()
                    if item and item.get("title"):
                        results.append({
                            "id": item.get("id"),
                            "title": item.get("title"),
                            "url": item.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
                            "score": item.get("score", 0),
                            "by": item.get("by"),
                            "time": item.get("time"),
                            "comments": item.get("descendants", 0),
                            "source": "hackernews",
                        })
                except Exception:
                    continue
            CACHE[cache_key] = results
            return results
    except Exception as e:
        logger.error("HN error: %s", e)
        return []


async def get_reddit(subreddit: str = "technology", limit: int = 25) -> List[Dict[str, Any]]:
    cache_key = f"reddit:{subreddit}:{limit}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": "00o-bot/1.0"}) as client:
            r = await client.get(REDDIT_RSS.format(subreddit=subreddit))
            if r.status_code != 200:
                return []
            root = ET.fromstring(r.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            results = []
            for entry in root.findall("atom:entry", ns)[:limit]:
                title = entry.find("atom:title", ns)
                link = entry.find("atom:link", ns)
                author = entry.find("atom:author/atom:name", ns)
                results.append({
                    "title": title.text if title is not None else "",
                    "url": link.get("href") if link is not None else "",
                    "author": author.text if author is not None else "",
                    "source": f"reddit:r/{subreddit}",
                })
            CACHE[cache_key] = results
            return results
    except Exception as e:
        logger.error("Reddit error: %s", e)
        return []


async def get_rss_feed(url: str, limit: int = 15) -> List[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            r = await client.get(url)
            if r.status_code != 200:
                return []
            root = ET.fromstring(r.content)
            results = []
            for item in root.findall(".//item")[:limit]:
                title = item.find("title")
                link = item.find("link")
                desc = item.find("description")
                pub = item.find("pubDate")
                results.append({
                    "title": title.text if title is not None else "",
                    "url": link.text if link is not None else "",
                    "description": (desc.text or "")[:200] if desc is not None else "",
                    "published": pub.text if pub is not None else "",
                    "source": url,
                })
            return results
    except Exception as e:
        logger.error("RSS error: %s: %s", url, e)
        return []


async def get_aggregated_news(query: Optional[str] = None) -> Dict[str, Any]:
    tasks = [
        get_hackernews(20),
        get_reddit("technology", 15),
        get_reddit("worldnews", 15),
    ]
    for feed in RSS_FEEDS[:3]:
        tasks.append(get_rss_feed(feed, 10))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    hn = results[0] if isinstance(results[0], list) else []
    red_tech = results[1] if isinstance(results[1], list) else []
    red_world = results[2] if isinstance(results[2], list) else []
    rss_items: List[Dict[str, Any]] = []
    for r in results[3:]:
        if isinstance(r, list):
            rss_items.extend(r)
    all_items = hn + red_tech + red_world + rss_items
    if query:
        q = query.lower()
        all_items = [it for it in all_items if q in (it.get("title") or "").lower()]
    return {
        "hackernews": hn,
        "reddit_tech": red_tech,
        "reddit_world": red_world,
        "rss": rss_items[:30],
        "all": all_items[:50],
        "query": query,
    }
