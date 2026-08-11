"""
Translation service using MyMemory free API.
No API key required (5000 chars/day anonymous).
"""

import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

MYMEMORY_URL = "https://api.mymemory.translated.net/get"
CACHE: Dict[str, Dict[str, Any]] = {}


async def translate(text: str, target: str = "en", source: Optional[str] = None) -> Dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {"error": "Empty text"}
    if len(text) > 500:
        return {"error": "Text too long. Max 500 chars (MyMemory free tier)"}
    cache_key = f"{source or 'auto'}:{target}:{text}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"q": text, "langpair": f"{source or 'auto'}|{target}"}
            r = await client.get(MYMEMORY_URL, params=params)
            data = r.json()
            if data.get("responseStatus") == 200:
                result = {
                    "source": data.get("match", {}).get("source", source or "auto"),
                    "target": target,
                    "translated": data.get("responseData", {}).get("translatedText", ""),
                    "match": data.get("match", {}).get("match", 0),
                    "original": text,
                }
                CACHE[cache_key] = result
                return result
            return {"error": data.get("responseDetails", "Translation failed")}
    except Exception as e:
        logger.error("Translate error: %s", e)
        return {"error": str(e)}


async def detect_language(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {"error": "Empty text"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(MYMEMORY_URL, params={"q": text[:500], "langpair": "auto|en"})
            data = r.json()
            return {
                "text": text,
                "detected": data.get("match", {}).get("source", "unknown"),
                "match_quality": data.get("match", {}).get("match", 0),
            }
    except Exception as e:
        return {"error": str(e)}
