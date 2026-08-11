"""
Currency exchange service using Frankfurter (free, ECB-based, no API key).
Also includes crypto via CoinGecko public API.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)

FRANKFURTER_LATEST = "https://api.frankfurter.app/latest"
FRANKFURTER_TIMESERIES = "https://api.frankfurter.app/{start}..{end}"
FRANKFURTER_CURRENCIES = "https://api.frankfurter.app/currencies"
COINGECKO_PRICE = "https://api.coingecko.com/api/v3/simple/price"
CACHE: Dict[str, Dict[str, Any]] = {}


async def get_currencies() -> Dict[str, str]:
    if "list" in CACHE:
        return CACHE["list"]
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(FRANKFURTER_CURRENCIES)
            data = r.json()
            CACHE["list"] = data
            return data
    except Exception as e:
        logger.error("Currencies error: %s", e)
        return {}


async def get_rate(base: str = "USD", target: str = "EUR", amount: float = 1.0) -> Dict[str, Any]:
    base = (base or "USD").upper()
    target = (target or "EUR").upper()
    cache_key = f"rate:{base}:{target}"
    if cache_key in CACHE:
        data = CACHE[cache_key]
    else:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                r = await client.get(FRANKFURTER_LATEST, params={"from": base, "to": target})
                data = r.json()
                CACHE[cache_key] = data
        except Exception as e:
            return {"error": str(e)}
    rates = data.get("rates", {})
    rate = rates.get(target, 1.0)
    return {
        "base": base,
        "target": target,
        "rate": rate,
        "amount": amount,
        "converted": round(amount * rate, 6),
        "date": data.get("date"),
    }


async def get_crypto(ids: List[str] = None, vs: str = "usd") -> Dict[str, Any]:
    if ids is None:
        ids = ["bitcoin", "ethereum", "solana", "toncoin", "binancecoin"]
    ids_str = ",".join(ids)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(COINGECKO_PRICE, params={"ids": ids_str, "vs_currencies": vs})
            data = r.json()
            return {"vs_currency": vs, "data": data, "ids": ids}
    except Exception as e:
        return {"error": str(e)}


async def get_timeseries(base: str = "USD", target: str = "UZS", days: int = 30) -> Dict[str, Any]:
    base = (base or "USD").upper()
    target = (target or "UZS").upper()
    end = datetime.utcnow().date()
    start = end - timedelta(days=min(days, 365))
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(FRANKFURTER_TIMESERIES.format(start=start, end=end),
                                 params={"from": base, "to": target})
            data = r.json()
            return {
                "base": base,
                "target": target,
                "start": str(start),
                "end": str(end),
                "series": data.get("rates", {}),
            }
    except Exception as e:
        return {"error": str(e)}
