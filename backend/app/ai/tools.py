"""30+ AI Tools - GroqCloud Powered"""
import os
from groq import Groq
from typing import Dict, Any

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS = {
    "fast": "llama-3.1-8b-instant",
    "balanced": "llama-3.3-70b-versatile",
    "smart": "llama-3.3-70b-versatile",
    "code": "llama-3.3-70b-versatile",
    "creative": "mixtral-8x7b-32768",
    "deepseek": "deepseek-r1-distill-llama-70b",
}

async def call_groq(prompt: str, model: str = "balanced", system: str = None) -> str:
    """Groq API chaqirish"""
    try:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model=MODELS.get(model, MODELS["balanced"]),
            messages=messages, temperature=0.7, max_tokens=4096,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Xatolik: {str(e)}"


# 1. Chat
async def ai_chat(input: str, language: str = "uz") -> str:
    return await call_groq(input, "balanced", f"Sen foydalanuvchiga yordam beruvchi AI assistantsan. {language} tilida javob ber.")


# 2. Startup Ideas
async def startup_ideas(input: str, language: str = "uz") -> str:
    system = f"Sen professional startup advisor san. {language} tilida 10 ta kreativ startap g'oyasi ber."
    prompt = f"Quyidagi soha uchun 10 ta innovatsion startap g'oyasi:\n\nSoha: {input}\n\nHar bir g'oya uchun:\n1. Nomi\n2. Muammo\n3. Yechim\n4. Bozor\n5. Daromad modeli"
    return await call_groq(prompt, "creative", system)


# 3. Business Plan
async def business_plan(input: str, language: str = "uz") -> str:
    system = f"Sen biznes konsultant san. Professional biznes reja yoz. {language} tilida."
    prompt = f"""Quyidagi startap uchun to'liq biznes reja yozing:

Startap: {input}

Quyidagilarni o'z ichiga olsin:
1. Executive Summary
2. Market Analysis (TAM, SAM, SOM)
3. Competitive Analysis
4. SWOT Analysis
5. Business Model
6. Marketing Strategy
7. Financial Projections (3 yil)
8. Funding Requirements
9. Team Structure
10. Risk Analysis
11. Milestones & Timeline"""
    return await call_groq(prompt, "smart", system)


# 4. Pitch Deck
async def pitch_deck(input: str, language: str = "uz") -> str:
    system = f"Sen pitch deck mutaxassisi san. Investorlar uchun ta'sirli pitch yoz. {language} tilida."
    prompt = f"""Quyidagi startap uchun 10 slaydlik pitch deck kontenti yozing:

Startap: {input}

Har bir slayd uchun:
- Sarlavha
- Asosiy mazmun (3-5 bullet point)
- Dizayn tavsiyasi"""
    return await call_groq(prompt, "creative", system)


# 5. SWOT
async def swot_analysis(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi startap yoki kompaniyaning SWOT tahlilini qiling:\n\n{input}",
        "balanced", f"Professional biznes tahlilchi san. {language} tilida."
    )


# 6. Business Name
async def business_name(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"'{input}' sohasi uchun 20 ta kreativ biznes nomi taklif qiling. Har biri uchun ma'no.",
        "creative", f"Brending mutaxassisi san. {language} tilida."
    )


# 7. Logo Prompt
async def logo_prompt(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi brend uchun AI image generation uchun batafsil prompt yozing (ingliz tilida):\n\nBrend: {input}",
        "creative", "Sen AI art prompt muhandisi san."
    )


# 8. Domain
async def domain_suggestion(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"'{input}' uchun 30 ta domen varianti (.com, .io, .uz, .co, .net, .app).",
        "fast", "Domen mutaxassisi san."
    )


# 9. Resume
async def resume_builder(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi ma'lumotlar asosida professional CV yarating:\n\n{input}",
        "balanced", f"HR mutaxassisi san. {language} tilida."
    )


# 10. Cover Letter
async def cover_letter(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi ma'lumotlar asosida cover letter yozing:\n\n{input}",
        "balanced", f"Career coach san. {language} tilida."
    )


# 11. Job Description
async def job_description(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi lavozim uchun professional ish tavsifi yozing:\n\n{input}",
        "balanced", f"Recruiter san. {language} tilida."
    )


# 12. Marketing
async def marketing_strategy(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi biznes uchun marketing strategiyasi:\n\n{input}\n\n- Target audience\n- Positioning\n- 4P\n- Digital\n- KPIs",
        "smart", f"Marketing strateg san. {language} tilida."
    )


# 13. SEO
async def seo_generator(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"'{input}' uchun SEO kontent yarating: title, meta, H1/H2, kalit so'zlar.",
        "balanced", f"SEO mutaxassisi san. {language} tilida."
    )


# 14. Blog Post
async def blog_post(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"'{input}' mavzusida 1500 so'zli blog post yozing. SEO optimized.",
        "creative", f"Content writer san. {language} tilida."
    )


# 15. Translate
async def translate_text(input: str, target_lang: str = "en", source_lang: str = "auto") -> str:
    return await call_groq(
        f"Quyidagi matnni {target_lang} tiliga tarjima qiling:\n\n{input}",
        "balanced", f"Professional tarjimon san. {target_lang} tilida."
    )


# 16. Summarize
async def summarize(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi matnni 3 xil usulda xulosalang:\n\n{input}",
        "balanced", f"Editor san. {language} tilida."
    )


# 17. Code Generator
async def code_generator(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi talab uchun to'liq kod yozing:\n\n{input}\n\nKommentlangan, best practices, error handling.",
        "code", "Senior software engineer san."
    )


# 18. Bug Fixer
async def fix_bug(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi kodda xatolik toping va tuzating:\n\n{input}",
        "code", "Debugging mutaxassisi san."
    )


# 19. Code Review
async def code_review(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi kodni ko'rib chiqing:\n\n{input}\n\nQuality, Performance, Security, Readability.",
        "code", "Senior code reviewer san."
    )


# 20. API Docs
async def api_docs(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi API uchun OpenAPI 3.0 dokumentatsiya:\n\n{input}",
        "balanced", "API documentation mutaxassisi san."
    )


# 21. SQL
async def sql_generator(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi talab uchun SQL query:\n\n{input}\n\nOptimallashtirilgan.",
        "code", "Database expert san."
    )


# 22. UI
async def ui_generator(input: str, language: str = "en") -> str:
    return await call_groq(
        f"Quyidagi talab uchun Tailwind+React komponent:\n\n{input}",
        "code", "Senior frontend engineer san."
    )


# 23. Planner
async def project_planner(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi loyiha uchun reja:\n\n{input}\n\nPhases, Milestones, Timeline, Budget.",
        "smart", f"Project manager san. {language} tilida."
    )


# 24. Brainstorm
async def brainstorm(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"'{input}' mavzusida 50 ta kreativ g'oya.",
        "creative", f"Kreativ fikrlash san. {language} tilida."
    )


# 25. Financial
async def financial_analysis(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Moliyaviy tahlil:\n\n{input}\n\nRevenue, Cost, Profit, ROI.",
        "smart", f"Financial analyst san. {language} tilida."
    )


# 26. Market
async def market_research(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Bozor tadqiqoti:\n\n{input}\n\nTAM, SAM, SOM, Trends, Competitors.",
        "smart", f"Market researcher san. {language} tilida."
    )


# 27. Competitor
async def competitor_analysis(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"5 ta raqobatchini tahlil qiling:\n\n{input}",
        "smart", f"Strategy consultant san. {language} tilida."
    )


# 28. Legal
async def legal_document(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Quyidagi yuridik hujjat uchun shablon:\n\n{input}",
        "balanced", f"Yurist san. {language} tilida."
    )


# 29. Email
async def email_writer(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Professional email yozing:\n\n{input}",
        "balanced", f"Email copywriter san. {language} tilida."
    )


# 30. Social Media
async def social_media_post(input: str, language: str = "uz") -> str:
    return await call_groq(
        f"Ijtimoiy tarmoq postlari:\n\n{input}\n\nInstagram, Twitter, LinkedIn, Facebook, TikTok, YouTube.",
        "creative", f"SMM mutaxassisi san. {language} tilida."
    )


TOOLS_MAP = {
    "chat": ai_chat, "startup-ideas": startup_ideas, "business-plan": business_plan,
    "pitch-deck": pitch_deck, "swot": swot_analysis, "business-name": business_name,
    "logo-prompt": logo_prompt, "domain": domain_suggestion, "resume": resume_builder,
    "cover-letter": cover_letter, "job-description": job_description, "marketing": marketing_strategy,
    "seo": seo_generator, "blog": blog_post, "translate": translate_text, "summarize": summarize,
    "code": code_generator, "fix-bug": fix_bug, "code-review": code_review, "api-docs": api_docs,
    "sql": sql_generator, "ui": ui_generator, "planner": project_planner, "brainstorm": brainstorm,
    "financial": financial_analysis, "market": market_research, "competitor": competitor_analysis,
    "legal": legal_document, "email": email_writer, "social": social_media_post,
}
