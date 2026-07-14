"""AI tools - 30+ functions"""
from .groq_client import groq_chat, groq_translate


async def business_plan(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Biznes reja yozing (professional, batafsil, {lang} tilida): {input}\n\n1. Xulosa 2. Bozor tahlili 3. Mahsulot 4. Marketing 5. Moliyaviy reja 6. Jamoa 7. Xavflar", lang)


async def pitch_deck(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Pitch deck yarating (10 slayd, professional, {lang}): {input}", lang)


async def startup_ideas(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Berilgan soha bo'yicha 10 ta startap g'oya yarating ({lang}): {input}", lang)


async def swot(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"SWOT tahlil qiling (batafsil, {lang}): {input}", lang)


async def business_name(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Biznes nomi taklif qiling (15 ta, kreativ, {lang}): {input}", lang)


async def logo_prompt(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Logotip yaratish uchun batafsil prompt yozing (English): {input}", "en")


async def domain(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Biznes uchun 20 ta domen nomi taklif qiling: {input}", lang)


async def resume(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Professional resume yarating (ATS-friendly, {lang}): {input}", lang)


async def cover_letter(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Cover letter yozing (professional, {lang}): {input}", lang)


async def job_description(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Ish tavsifi yozing (batafsil, {lang}): {input}", lang)


async def marketing(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Marketing strategiyasi yarating (360°, {lang}): {input}", lang)


async def seo(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"SEO optimallashtirish ({lang}): {input}", lang)


async def blog(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Blog post yozing (1500+ so'z, SEO-friendly, {lang}): {input}", lang)


async def social(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Social media kontent yarating (Instagram, Telegram, Facebook, 5 ta post, {lang}): {input}", lang)


async def email(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Professional email yozing (3 variant, {lang}): {input}", lang)


async def code(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Professional kod yozing (clean, documented, {input})", "en")


async def fix_bug(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Bug ni toping va tuzating: {input}", "en")


async def code_review(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Kod review qiling (performance, security, best practices): {input}", "en")


async def api_docs(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"API documentation yozing (OpenAPI format): {input}", "en")


async def sql(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"SQL query yozing (optimallashtirilgan): {input}", "en")


async def ui(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"UI komponent yarating (React + TailwindCSS): {input}", "en")


async def summarize(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Matnni qisqacha xulosa qiling (3-5 bullet, {lang}): {input}", lang)


async def brainstorm(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Brainstorming qiling (20 ta kreativ g'oya, {lang}): {input}", lang)


async def planner(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Loyiha rejasi tuzing (timeline, milestones, {lang}): {input}", lang)


async def financial(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Moliyaviy tahlil qiling (P&L, ROI, {lang}): {input}", lang)


async def market(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Bozor tadqiqoti (TAM, SAM, SOM, {lang}): {input}", lang)


async def competitor(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Raqobatchilar tahlili (5 ta raqib, {lang}): {input}", lang)


async def legal(input: str, lang: str = "uz") -> str:
    return await groq_chat(f"Yuridik maslahat bering (O'zbekiston, {lang}): {input}", lang)


async def translate(text: str, target_lang: str = "en") -> str:
    return await groq_translate(text, target_lang)


async def chat(input: str, lang: str = "uz") -> str:
    return await groq_chat(input, lang)


TOOLS_MAP = {
    "chat": chat, "business-plan": business_plan, "pitch-deck": pitch_deck, "startup-ideas": startup_ideas,
    "swot": swot, "business-name": business_name, "logo-prompt": logo_prompt, "domain": domain,
    "resume": resume, "cover-letter": cover_letter, "job-description": job_description,
    "marketing": marketing, "seo": seo, "blog": blog, "social": social, "email": email,
    "code": code, "fix-bug": fix_bug, "code-review": code_review, "api-docs": api_docs,
    "sql": sql, "ui": ui, "summarize": summarize, "brainstorm": brainstorm, "planner": planner,
    "financial": financial, "market": market, "competitor": competitor, "legal": legal, "translate": translate,
}
