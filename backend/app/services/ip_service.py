"""
IP Geolocation service - get country, city, ISP for any IP address.
Free APIs: ip-api.com, ipapi.co
"""

import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
IPAPI_URL = "https://ipapi.co/{ip}/json/"
CACHE: Dict[str, Dict[str, Any]] = {}


async def get_ip_info(ip: Optional[str] = None) -> Dict[str, Any]:
    target = ip or ""
    if target in CACHE:
        return CACHE[target]
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            url = IP_API_URL.format(ip=target)
            r = await client.get(url)
            data = r.json()
            if data.get("status") == "success":
                CACHE[target] = data
                return data
    except Exception as e:
        logger.warning("ip-api failed: %s, trying fallback", e)
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            url = IPAPI_URL.format(ip=target or "")
            r = await client.get(url)
            data = r.json()
            if not data.get("error"):
                CACHE[target] = data
                return data
    except Exception as e:
        logger.error("ipapi.co failed: %s", e)
    return {"status": "fail", "message": "Could not resolve IP"}
