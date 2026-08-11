"""
WHOIS service - domain registration info.
Uses RDAP (Registration Data Access Protocol) - the modern replacement.
"""

import logging
from typing import Any, Dict

import httpx

logger = logging.getLogger(__name__)

RDAP_BOOTSTRAP = "https://rdap.org/domain/{domain}"
CACHE: Dict[str, Dict[str, Any]] = {}


async def whois_lookup(domain: str) -> Dict[str, Any]:
    domain = (domain or "").strip().lower()
    if not domain or "." not in domain:
        return {"error": "Invalid domain"}
    if domain in CACHE:
        return CACHE[domain]
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            r = await client.get(RDAP_BOOTSTRAP.format(domain=domain))
            if r.status_code == 200:
                data = r.json()
                events = {e.get("eventAction"): e.get("eventDate") for e in data.get("events", [])}
                entities = []
                for ent in data.get("entities", []):
                    entities.append({
                        "name": ent.get("handle"),
                        "roles": ent.get("roles", []),
                        "email": _extract_email(ent.get("vcardArray")),
                    })
                result = {
                    "domain": domain,
                    "registrar": data.get("port43") or (entities[0]["name"] if entities else None),
                    "status": data.get("status", []),
                    "nameservers": [ns.get("ldhName") for ns in data.get("nameservers", []) if ns.get("ldhName")],
                    "created": events.get("registration"),
                    "updated": events.get("last changed") or events.get("last update"),
                    "expires": events.get("expiration"),
                    "entities": entities,
                    "raw": data,
                }
                CACHE[domain] = result
                return result
            return {"error": f"RDAP returned {r.status_code}"}
    except Exception as e:
        logger.error("WHOIS error: %s", e)
        return {"error": str(e)}


def _extract_email(vcard_array):
    if not vcard_array or not isinstance(vcard_array, list):
        return None
    for vcard in vcard_array[1:]:
        for field in vcard:
            if isinstance(field, list) and field[0] == "email":
                return field[3]
    return None
