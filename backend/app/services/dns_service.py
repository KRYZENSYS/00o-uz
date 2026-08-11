"""
DNS lookup service - A, AAAA, MX, TXT, NS, CNAME, SOA records.
Uses Google DNS-over-HTTPS for free, no rate limits.
"""

import logging
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)

GOOGLE_DNS = "https://dns.google/resolve"
CACHE: Dict[str, Dict[str, Any]] = {}

RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CNAME", "SOA", "PTR", "SRV"]


async def dns_lookup(domain: str, record_type: str = "A") -> Dict[str, Any]:
    domain = (domain or "").strip().lower()
    record_type = (record_type or "A").upper()
    if record_type not in RECORD_TYPES:
        return {"error": f"Invalid type. Use one of: {RECORD_TYPES}"}
    cache_key = f"{domain}:{record_type}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(GOOGLE_DNS, params={"name": domain, "type": record_type})
            data = r.json()
            if data.get("Status") == 0:
                result = {
                    "domain": domain,
                    "type": record_type,
                    "answers": data.get("Answer", []),
                    "raw": data,
                }
                CACHE[cache_key] = result
                return result
            return {"error": "DNS query failed", "status": data.get("Status"), "raw": data}
    except Exception as e:
        logger.error("DNS lookup error: %s", e)
        return {"error": str(e)}


async def bulk_dns(domain: str) -> Dict[str, List[Any]]:
    domain = (domain or "").strip().lower()
    results: Dict[str, List[Any]] = {}
    for rtype in ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]:
        res = await dns_lookup(domain, rtype)
        results[rtype] = res.get("answers", [])
    return results
