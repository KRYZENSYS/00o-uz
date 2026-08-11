"""
Weather service using Open-Meteo (free, no API key, no rate limit).
https://open-meteo.com/
"""

import logging
from typing import Any, Dict

import httpx

logger = logging.getLogger(__name__)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
CACHE: Dict[str, Dict[str, Any]] = {}


async def geocode(city: str) -> Dict[str, Any]:
    city = (city or "").strip()
    if not city:
        return {"error": "Empty city"}
    cache_key = f"geo:{city.lower()}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(GEOCODE_URL, params={"name": city, "count": 1, "language": "en", "format": "json"})
            data = r.json()
            if data.get("results"):
                first = data["results"][0]
                result = {
                    "name": first.get("name"),
                    "country": first.get("country"),
                    "lat": first.get("latitude"),
                    "lon": first.get("longitude"),
                    "timezone": first.get("timezone"),
                }
                CACHE[cache_key] = result
                return result
            return {"error": "City not found"}
    except Exception as e:
        logger.error("Geocode error: %s", e)
        return {"error": str(e)}


async def get_weather(city: str) -> Dict[str, Any]:
    loc = await geocode(city)
    if "error" in loc:
        return loc
    lat, lon = loc["lat"], loc["lon"]
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum",
                "timezone": loc.get("timezone", "auto"),
                "forecast_days": 7,
            }
            r = await client.get(WEATHER_URL, params=params)
            data = r.json()
            if "error" in data:
                return {"error": data["error"]}
            current = data.get("current", {})
            daily = data.get("daily", {})
            return {
                "location": {"city": loc["name"], "country": loc["country"], "lat": lat, "lon": lon},
                "current": {
                    "temperature": current.get("temperature_2m"),
                    "feels_like": current.get("apparent_temperature"),
                    "humidity": current.get("relative_humidity_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_direction": current.get("wind_direction_10m"),
                    "is_day": bool(current.get("is_day")),
                    "weather_code": current.get("weather_code"),
                    "precipitation": current.get("precipitation"),
                },
                "forecast": [
                    {
                        "date": (daily.get("time") or [None])[i],
                        "weather_code": (daily.get("weather_code") or [None])[i],
                        "temp_max": (daily.get("temperature_2m_max") or [None])[i],
                        "temp_min": (daily.get("temperature_2m_min") or [None])[i],
                        "sunrise": (daily.get("sunrise") or [None])[i],
                        "sunset": (daily.get("sunset") or [None])[i],
                        "uv_index": (daily.get("uv_index_max") or [None])[i],
                        "precipitation": (daily.get("precipitation_sum") or [None])[i],
                    }
                    for i in range(len(daily.get("time", [])))
                ],
                "timezone": data.get("timezone"),
            }
    except Exception as e:
        logger.error("Weather error: %s", e)
        return {"error": str(e)}


def weather_code_to_text(code: int) -> Dict[str, str]:
    codes = {
        0: ("Clear sky", "\u2600\ufe0f"), 1: ("Mainly clear", "\ud83c\udf24\ufe0f"), 2: ("Partly cloudy", "\u26c5"), 3: ("Overcast", "\u2601\ufe0f"),
        45: ("Fog", "\ud83c\udf2b\ufe0f"), 48: ("Rime fog", "\ud83c\udf2b\ufe0f"),
        51: ("Light drizzle", "\ud83c\udf26\ufe0f"), 53: ("Drizzle", "\ud83c\udf26\ufe0f"), 55: ("Dense drizzle", "\ud83c\udf27\ufe0f"),
        61: ("Slight rain", "\ud83c\udf26\ufe0f"), 63: ("Rain", "\ud83c\udf27\ufe0f"), 65: ("Heavy rain", "\ud83c\udf27\ufe0f"),
        71: ("Slight snow", "\ud83c\udf28\ufe0f"), 73: ("Snow", "\ud83c\udf28\ufe0f"), 75: ("Heavy snow", "\u2744\ufe0f"),
        80: ("Rain showers", "\ud83c\udf26\ufe0f"), 81: ("Rain showers", "\ud83c\udf27\ufe0f"), 82: ("Violent showers", "\u26c8\ufe0f"),
        95: ("Thunderstorm", "\u26c8\ufe0f"), 96: ("Thunderstorm + hail", "\u26c8\ufe0f"), 99: ("Thunderstorm + heavy hail", "\u26c8\ufe0f"),
    }
    return {"text": codes.get(code, ("Unknown", "\u2753"))[0], "emoji": codes.get(code, ("Unknown", "\u2753"))[1]}
