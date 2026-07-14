"""
GroqCloud AI Service
OpenAI-compatible interface with streaming, history, retry, error handling
"""
import time
import asyncio
from typing import List, Dict, Optional, AsyncGenerator
from groq import AsyncGroq
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings


class GroqService:
    """Main AI service powered by GroqCloud (OpenAI-compatible)"""

    SUPPORTED_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "deepseek-r1-distill-llama-70b",
        "qwen-2.5-32k-instruct",
    ]

    LANGUAGE_INSTRUCTIONS = {
        "uz": "Javobni O'ZBEK tilida yoz. Professional va tushunarli bo'lsin.",
        "ru": "Отвечай на РУССКОМ языке. Будь профессиональным и понятным.",
        "en": "Respond in ENGLISH. Be professional and clear."
    }

    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY, base_url=settings.GROQ_BASE_URL)
        self.default_model = settings.GROQ_DEFAULT_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        language: str = "uz",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
    ):
        model = model or self.default_model
        if model not in self.SUPPORTED_MODELS:
            model = self.default_model

        if messages and messages[0].get("role") != "system":
            messages.insert(0, {
                "role": "system",
                "content": self.LANGUAGE_INSTRUCTIONS.get(language, self.LANGUAGE_INSTRUCTIONS["uz"])
            })

        start = time.time()
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            duration = int((time.time() - start) * 1000)
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "tokens": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "duration_ms": duration,
            }
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise

    async def generate_business_plan(self, idea: str, language: str = "uz") -> str:
        prompt = f"""Quyidagi startap g'oyasi uchun batafsil biznes reja yarating:

G'OYA: {idea}

Biznes rejada quyidagilar bo'lsin:
1. Xulosa
2. Bozor tahlili
3. Mahsulot tavsifi
4. Marketing strategiyasi
5. Moliyaviy prognoz
6. Jamoa
7. Xavflar

Professional formatda, markdown."""
        result = await self.chat(messages=[{"role": "user", "content": prompt}], language=language, max_tokens=3000)
        return result["content"]

    async def generate_startup_ideas(self, interests: str, language: str = "uz") -> str:
        prompt = f"Quyidagi sohada 10 ta innovative startap g'oyalari taklif qil:\n\nSOHA: {interests}\n\nHar bir g'oya uchun: nomi, tavsif, auditoriya, daromad modeli. Markdown formatda."
        result = await self.chat(messages=[{"role": "user", "content": prompt}], language=language, max_tokens=2500)
        return result["content"]

    async def analyze_startup(self, description: str, language: str = "uz") -> str:
        prompt = f"Quyidagi startapni tahlil qil (SWOT + tavsiyalar):\n\n{description}\n\nO'zbek tilida, professional formatda."
        result = await self.chat(messages=[{"role": "user", "content": prompt}], language=language, max_tokens=2000)
        return result["content"]

    async def translate(self, text: str, target_language: str) -> str:
        lang_names = {"uz": "O'zbek", "ru": "Rus", "en": "Ingliz"}
        prompt = f"Quyidagi matnni {lang_names.get(target_language)} tiliga tarjima qil:\n\n{text}"
        result = await self.chat(messages=[{"role": "user", "content": prompt}], language=target_language)
        return result["content"]

    async def summarize(self, text: str, language: str = "uz") -> str:
        prompt = f"Quyidagi matnni qisqacha bayon qil:\n\n{text}"
        result = await self.chat(messages=[{"role": "user", "content": prompt}], language=language, max_tokens=1000)
        return result["content"]

    async def get_models(self) -> List[Dict]:
        return [{"id": m, "name": m, "provider": "groq"} for m in self.SUPPORTED_MODELS]


groq_service = GroqService()
