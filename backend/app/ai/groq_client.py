"""Groq AI client"""
import httpx
from ..core.config import settings


async def groq_chat(prompt: str, language: str = "uz", max_tokens: int = 4000, temperature: float = 0.7) -> str:
    if not settings.GROQ_API_KEY:
        return f"[AI Mock - GROQ_API_KEY yo'q]\n\nPrompt: {prompt[:300]}..."

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": f"Siz yordamchi AI assistantsiz. Javobni {language} tilida, professional va batafsil qilib yozing. Markdown formatida."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": max_tokens, "temperature": temperature
                }
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"❌ AI xatolik: {r.text[:200]}"
    except Exception as e:
        return f"❌ Ulanish xatoligi: {str(e)}"


async def groq_translate(text: str, target_lang: str) -> str:
    lang_map = {"en": "English", "ru": "Russian", "uz": "Uzbek", "tr": "Turkish", "ar": "Arabic", "es": "Spanish", "fr": "French", "de": "German", "zh": "Chinese", "ja": "Japanese", "ko": "Korean"}
    target = lang_map.get(target_lang, target_lang)
    prompt = f"Quyidagi matnni {target} tiliga professional tarjima qiling. Faqat tarjimani qaytaring:\n\n{text}"
    return await groq_chat(prompt, "en", max_tokens=len(text) * 2)
