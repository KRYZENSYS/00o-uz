"""
Vercel serverless AI chat endpoint.
Uses HuggingFace free inference (router.huggingface.co) with smart fallback.

Env:
  HF_TOKEN (optional, for higher rate limits)
  HUGGINGFACE_MODEL (default: meta-llama/Meta-Llama-3-8B-Instruct)
  GROQ_API_KEY (fallback)
  GROQ_MODEL (fallback, default: llama-3.3-70b-versatile)
"""

import json
import os
import re
import time
import logging
from typing import Any, Dict, List, Optional
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("ai-chat")

HF_TOKEN = os.getenv("HF_TOKEN", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

HF_API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"
HF_FEATHERLESS_URL = "https://api.featherless.ai/v1/chat/completions"

# System prompt templates per language
SYSTEM_PROMPTS = {
    "uz": "Siz 00o.uz platformasining AI yordamchisiz. O'zbek tilida, qisqa va aniq javob bering. Foydalanuvchiga do'stona va professional yordam bering.",
    "ru": "Вы AI-помощник платформы 00o.uz. Отвечайте на русском языке кратко и точно. Будьте дружелюбны и профессиональны.",
    "en": "You are the AI assistant of the 00o.uz platform. Respond in English concisely and accurately. Be friendly and professional.",
}

# In-memory rate limiter (per-IP, 20 req / 60s)
RATE_LIMIT_BUCKET: Dict[str, List[float]] = {}
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 20

# Simple in-memory conversation cache
CONVERSATION_CACHE: Dict[str, List[Dict[str, str]]] = {}
CACHE_MAX = 200
CACHE_TTL = 1800  # 30 min

# Smart fallback knowledge base
SMART_FALLBACK: Dict[str, Dict[str, str]] = {
    "uz": {
        "salom": "Salom! Men 00o.uz AI yordamchisiman. Sizga qanday yordam bera olaman?",
        "kim san": "Men 00o.uz platformasining AI yordamchisiman. Frontend Next.js 15, backend FastAPI, AI GroqCloud da ishlayman.",
        "platforma": "00o.uz - bu startaplar, freelancerlar va investorlarni birlashtiruvchi O'zbekistonning eng yirik AI platformasi. Startup marketplace, jobs, AI chat, kurslar, live streaming va boshqa ko'p narsalar mavjud.",
        "qanday": "00o.uz da startap yaratishingiz, xizmat ko'rsatishingiz, ish topishingiz yoki investitsiya qilishingiz mumkin. Bosh sahifadan ro'yxatdan o'ting!",
        "narx": "Platforma bepul. Premium obuna 49,000 so'm/oy. AI tokenlar 100,000 so'm/1000 token.",
        "kontakt": "Telegram: @mira_support_team. Email: support@00o.uz",
        "yordam": "Men sizga sayt, startap, ish, AI chat yoki texnik masalalarda yordam bera olaman. Savol bering!",
    },
    "ru": {
        "привет": "Привет! Я AI-помощник 00o.uz. Чем могу помочь?",
        "кто ты": "Я AI-помощник платформы 00o.uz. Frontend Next.js 15, backend FastAPI, AI GroqCloud.",
        "платформа": "00o.uz - крупнейшая AI-платформа Узбекистана, объединяющая стартапы, фрилансеров и инвесторов.",
        "цена": "Платформа бесплатна. Premium подписка 49,000 сум/мес. AI токены 100,000 сум/1000 токенов.",
        "контакт": "Telegram: @mira_support_team. Email: support@00o.uz",
        "помощь": "Я могу помочь с сайтом, стартапами, работой, AI чатом или техническими вопросами.",
    },
    "en": {
        "hello": "Hello! I'm the 00o.uz AI assistant. How can I help you?",
        "who are you": "I'm the 00o.uz platform AI assistant. Built with Next.js 15, FastAPI, and GroqCloud AI.",
        "platform": "00o.uz is Uzbekistan's largest AI platform connecting startups, freelancers, and investors. Startup marketplace, jobs, AI chat, courses, live streaming.",
        "pricing": "Platform is free. Premium subscription 49,000 UZS/month. AI tokens 100,000 UZS/1000 tokens.",
        "contact": "Telegram: @mira_support_team. Email: support@00o.uz",
        "help": "I can help you with the site, startups, jobs, AI chat, or technical questions. Ask me anything!",
    },
}


def detect_language(text: str) -> str:
    """Detect language from text: uz/ru/en."""
    text = (text or "").lower().strip()
    if not text:
        return "en"
    cyr = len(re.findall(r"[\u0400-\u04ff]", text))
    lat = len(re.findall(r"[a-z]", text))
    uzbek_chars = len(re.findall(r"[o'\u2018\u2019g]", text))
    if cyr > lat:
        # Distinguish Russian vs Uzbek by specific letters
        uzbek_only = len(re.findall(r"[\u04b3\u04b1\u0493\u049b]", text))
        if uzbek_only > 0 or any(w in text for w in ["salom", "rahmat", "qanday", "nima"]):
            return "uz"
        return "ru"
    return "en"


def get_client_ip(headers: Dict[str, str]) -> str:
    return (
        headers.get("x-forwarded-for", "").split(",")[0].strip()
        or headers.get("x-real-ip", "")
        or "anonymous"
    )


def check_rate_limit(ip: str) -> bool:
    """Returns True if allowed, False if rate-limited."""
    now = time.time()
    bucket = RATE_LIMIT_BUCKET.setdefault(ip, [])
    bucket[:] = [t for t in bucket if now - t < RATE_LIMIT_WINDOW]
    if len(bucket) >= RATE_LIMIT_MAX:
        return False
    bucket.append(now)
    return True


def call_huggingface(messages: List[Dict[str, str]], model: str = None) -> Optional[Dict[str, Any]]:
    """Call HuggingFace free inference. Returns dict or None on error."""
    if not HF_TOKEN:
        logger.info("HF_TOKEN not set, skipping HuggingFace")
        return None
    payload = {"model": model or HUGGINGFACE_MODEL, "messages": messages, "max_tokens": 600, "temperature": 0.7}
    data = json.dumps(payload).encode()
    req = urlrequest.Request(
        HF_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {HF_TOKEN}",
        },
    )
    try:
        with urlrequest.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError, TimeoutError) as e:
        logger.warning("HF failed: %s", e)
        return None


def call_groq(messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """Call Groq API as fallback."""
    if not GROQ_API_KEY:
        return None
    payload = {"model": GROQ_MODEL, "messages": messages, "max_tokens": 600, "temperature": 0.7}
    data = json.dumps(payload).encode()
    req = urlrequest.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        },
    )
    try:
        with urlrequest.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError, TimeoutError) as e:
        logger.warning("Groq failed: %s", e)
        return None


def smart_fallback(message: str, lang: str) -> str:
    """Pattern-matched local response. Used when no AI is reachable."""
    msg = message.lower().strip()
    fallback = SMART_FALLBACK.get(lang, SMART_FALLBACK["en"])
    for key, value in fallback.items():
        if key in msg:
            return value
    # Generic responses
    generics = {
        "uz": "Yaxshi savol! Hozir AI provayderlari vaqtincha ishlamayapti. Iltimos, birozdan so'ng qayta urinib ko'ring yoki support@00o.uz ga yozing.",
        "ru": "Хороший вопрос! AI провайдеры временно недоступны. Попробуйте позже или напишите на support@00o.uz.",
        "en": "Good question! AI providers are temporarily unavailable. Please try again in a moment or email support@00o.uz.",
    }
    return generics.get(lang, generics["en"])


def build_messages(user_message: str, lang: str, history: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """Build OpenAI-style messages array."""
    system = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])
    messages = [{"role": "system", "content": system}]
    if history:
        messages.extend(history[-6:])  # last 3 turns
    messages.append({"role": "user", "content": user_message})
    return messages


def handler(request):
    """Vercel serverless entrypoint. /api/ai-chat"""
    try:
        if request.method == "OPTIONS":
            return _cors_response(204, {})
        if request.method != "POST":
            return _cors_response(405, {"error": "Method not allowed"})

        # Parse body
        body = request.body or b"{}"
        if isinstance(body, (bytes, bytearray)):
            body = body.decode("utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return _cors_response(400, {"error": "Invalid JSON body"})

        user_message = (data.get("message") or "").strip()
        if not user_message:
            return _cors_response(400, {"error": "Empty message"})
        if len(user_message) > 2000:
            return _cors_response(400, {"error": "Message too long (max 2000 chars)"})

        # Headers
        headers = {k.lower(): v for k, v in (request.headers or {}).items()}
        ip = get_client_ip(headers)
        if not check_rate_limit(ip):
            return _cors_response(429, {"error": "Rate limit exceeded. Max 20 requests/min."})

        # Detect language
        lang = data.get("lang") or detect_language(user_message)

        # Conversation cache key
        cache_key = f"{ip}:{hash(user_message[:30])}"
        history = CONVERSATION_CACHE.get(cache_key, [])
        messages = build_messages(user_message, lang, history)

        # Try HF first
        result = call_huggingface(messages)
        source = "huggingface"
        if not result:
            result = call_groq(messages)
            source = "groq"
        if not result or "choices" not in result:
            reply = smart_fallback(user_message, lang)
            return _cors_response(200, {
                "reply": reply,
                "lang": lang,
                "source": "smart-fallback",
                "model": "local-rules",
            })

        # Extract reply
        try:
            reply = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            reply = smart_fallback(user_message, lang)
            source = "smart-fallback"

        # Update cache
        CONVERSATION_CACHE[cache_key] = (history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": reply},
        ])[-10:]
        if len(CONVERSATION_CACHE) > CACHE_MAX:
            # Simple eviction: drop oldest
            for k in list(CONVERSATION_CACHE.keys())[:50]:
                CONVERSATION_CACHE.pop(k, None)

        return _cors_response(200, {
            "reply": reply,
            "lang": lang,
            "source": source,
            "model": HUGGINGFACE_MODEL if source == "huggingface" else GROQ_MODEL,
            "usage": result.get("usage"),
        })
    except Exception as e:
        logger.exception("AI chat error: %s", e)
        return _cors_response(500, {"error": "Internal error", "detail": str(e)})


def _cors_response(status: int, body: Dict[str, Any]):
    """Build Vercel response with CORS headers."""
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }
