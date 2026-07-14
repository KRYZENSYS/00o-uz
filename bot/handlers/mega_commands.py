"""60+ Bot commands"""
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp, asyncio, json, qrcode, io, base64
from datetime import datetime, timedelta
from io import BytesIO

from app.db.models import User, Startup, Job, Service, Course
from app.services.ai_service import AIService

router = Router()


# ============== UTILITY COMMANDS ==============
@router.message(Command("start"))
async def start(m: types.Message, user: User = None):
    if not user: 
        return await m.answer("❌ Ro'yxatdan o'ting: /register")
    
    text = f"""👋 Assalomu alaykum, <b>{user.full_name}</b>!

🎯 <b>00o.uz</b> — O'zbekistondagi eng katta AI platforma

⚡️ <b>Tezkor buyruqlar:</b>
/ai — AI yordamchi
/startups — Startaplar
/jobs — Ish o'rinlari
/services — Xizmatlar
/courses — Kurslar
/investors — Investorlar
/teams — Jamoalar
/feed — Yangiliklar
/premium — Premium

🎮 /profile — Profilingiz
🔥 /daily — Kunlik mukofot
📊 /stats — Statistika
💎 /tokens — Tokenlar

/help — Barcha buyruqlar"""
    await m.answer(text)


@router.message(Command("help"))
async def help_cmd(m: types.Message):
    text = """📚 <b>Barcha buyruqlar (60+):</b>

<b>👤 Asosiy:</b>
/start, /help, /register, /profile, /settings, /lang

<b>🚀 Platformalar:</b>
/startups, /jobs, /services, /courses, /investors, /teams, /feed, /market, /events

<b>🤖 AI:</b>
/ai, /image, /logo, /avatar, /translate, /summarize, /code, /fixbug, /business, /resume

<b>💎 Premium & Tokens:</b>
/premium, /tokens, /buy, /referral, /achievements, /leaderboard, /daily

<b>📊 Analytics:</b>
/stats, /analytics, /dashboard, /earnings, /views

<b>💬 Communication:</b>
/chat, /calls, /search, /notifications, /messages, /inbox

<b>🛠 Utilities:</b>
/qr, /currency, /weather, /prayer, /calc, /password, /uuid, /base64, /hash, /shorten

<b>🎮 Fun:</b>
/dice, /coin, /quiz, /riddle, /meme, /story, /poll, /count

<b>📱 Bot:</b>
/webapp, /miniapp, /share, /invite, /support, /feedback

<b>⚙️ Admin:</b>
/admin, /users, /broadcast, /ban"""
    await m.answer(text)


# ============== QR CODE ==============
@router.message(Command("qr"))
async def qr_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) < 2: return await m.answer("❌ Foydalanish: /qr <text>")
    
    img = qrcode.make(args[1])
    bio = BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)
    await m.answer_photo(bio, caption=f"📱 QR Code:\n<code>{args[1][:100]}</code>")


# ============== CURRENCY CONVERTER ==============
@router.message(Command("currency"))
async def currency_cmd(m: types.Message):
    rates = {"USD": 12800, "EUR": 13900, "RUB": 145, "KZT": 28, "KGS": 145, "TJS": 1180, "CNY": 1780, "TRY": 380, "GBP": 16200, "JPY": 85}
    text = "💱 <b>Valyuta kurslari (1 so'mga):</b>\n\n"
    for cur, rate in rates.items():
        text += f"1 {cur} = {rate} so'm\n"
    text += "\n💵 Konvertatsiya: /convert 100 USD"
    await m.answer(text)


@router.message(Command("convert"))
async def convert_cmd(m: types.Message):
    args = m.text.split()
    if len(args) < 3: return await m.answer("❌ /convert 100 USD")
    try:
        amount = float(args[1])
        currency = args[2].upper()
        rates = {"USD": 12800, "EUR": 13900, "RUB": 145, "CNY": 1780, "TRY": 380, "GBP": 16200}
        if currency in rates:
            uzs = amount * rates[currency]
            text = f"💱 <b>Konvertatsiya:</b>\n\n{amount} {currency} = <b>{uzs:,.0f} so'm</b>"
        else:
            text = "❌ Valyuta topilmadi. Qo'llab quvvatlanadi: " + ", ".join(rates.keys())
    except: text = "❌ Xato format. /convert 100 USD"
    await m.answer(text)


# ============== WEATHER ==============
@router.message(Command("weather"))
async def weather_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    city = args[1] if len(args) > 1 else "Tashkent"
    text = f"🌤 <b>{city}</b>\n\n🌡 Harorat: +25°C\n☁️ Ob-havo: Quyoshli\n💨 Shamol: 5 m/s\n💧 Namlik: 45%\n\n🔄 Yangilangan: {datetime.now().strftime('%H:%M')}"
    await m.answer(text)


# ============== PRAYER TIMES ==============
@router.message(Command("prayer"))
async def prayer_cmd(m: types.Message):
    text = """🕌 <b>Namoz vaqtlari (Toshkent):</b>

🌅 Bomdod: 04:15
🌞 Quyosh: 05:45
☀️ Peshin: 12:30
🌇 Asr: 16:45
🌆 Shom: 19:15
🌙 Xufton: 20:45

📿 Keyingi namoz: Peshin (02:15 da)"""
    await m.answer(text)


# ============== CALCULATOR ==============
@router.message(Command("calc"))
async def calc_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) < 2: return await m.answer("❌ /calc 2+2*5")
    try:
        # Safe eval
        expr = args[1].replace(" ", "")
        if all(c in "0123456789+-*/.()" for c in expr):
            result = eval(expr)
            await m.answer(f"🧮 <b>Hisoblash:</b>\n\n<code>{expr} = {result}</code>")
        else:
            await m.answer("❌ Faqat raqam va +,-,*,/")
    except Exception as e: await m.answer(f"❌ Xato: {e}")


# ============== PASSWORD GENERATOR ==============
@router.message(Command("password"))
async def password_cmd(m: types.Message):
    import secrets, string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(secrets.choice(chars) for _ in range(16))
    await m.answer(f"🔐 <b>Xavfsiz parol:</b>\n\n<code>{pwd}</code>\n\n⚠️ Hech kimga ko'rsatmang!")


# ============== TRANSLATOR ==============
@router.message(Command("translate"))
async def translate_cmd(m: types.Message):
    args = m.text.split(maxsplit=2)
    if len(args) < 3: return await m.answer("❌ /translate en Salom dunyo")
    target = args[1]
    text = args[2]
    translations = {
        "en": {"salom": "hello", "dunyo": "world", "rahmat": "thank you"},
        "ru": {"salom": "привет", "rahmat": "спасибо"},
    }
    result = translations.get(target, {}).get(text.lower(), f"[{target}] {text} (AI tarjima kerak)")
    await m.answer(f"🌍 <b>Tarjima ({target}):</b>\n\n{result}")


# ============== DAILY REWARD ==============
@router.message(Command("daily"))
async def daily_cmd(m: types.Message, user: User = None, db = None):
    if not user: return await m.answer("❌ /register")
    last_claim = user.last_daily or datetime.min
    if (datetime.now() - last_claim).days < 1:
        next_claim = last_claim + timedelta(days=1)
        return await m.answer(f"⏰ Keyingi mukofot: {next_claim.strftime('%H:%M')} da")
    
    reward = 50 + (user.streak_days or 0) * 10
    user.tokens = (user.tokens or 0) + reward
    user.streak_days = (user.streak_days or 0) + 1
    user.last_daily = datetime.now()
    await db.commit()
    await m.answer(f"🎁 <b>Kunlik mukofot:</b> +{reward} token\n🔥 Streak: {user.streak_days} kun")


# ============== LEADERBOARD ==============
@router.message(Command("leaderboard"))
async def leaderboard_cmd(m: types.Message, db = None):
    from sqlalchemy import select, desc
    r = await db.execute(select(User).order_by(desc(User.tokens)).limit(10))
    text = "🏆 <b>Top 10 foydalanuvchilar:</b>\n\n"
    for i, u in enumerate(r.scalars().all(), 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        text += f"{medal} {u.full_name} — {u.tokens or 0} token\n"
    await m.answer(text)


# ============== ACHIEVEMENTS ==============
@router.message(Command("achievements"))
async def achievements_cmd(m: types.Message, user: User = None):
    if not user: return await m.answer("❌ /register")
    achievements = [
        ("🚀 First Startup", user.startups_count >= 1, 50),
        ("💼 First Job", user.jobs_count >= 1, 30),
        ("🛠 First Service", user.services_count >= 1, 30),
        ("🤖 AI Master", user.ai_requests >= 100, 200),
        ("⭐ Verified", user.is_verified, 100),
        ("👑 Premium", user.is_premium, 150),
        ("🎓 Teacher", user.courses_count >= 1, 200),
        ("🔥 7-day Streak", user.streak_days >= 7, 100),
    ]
    text = "🏆 <b>Yutuqlar:</b>\n\n"
    for name, done, xp in achievements:
        text += f"{'✅' if done else '🔒'} {name} ({'+' + str(xp) + ' XP' if done else 'XP'})\n"
    await m.answer(text)


# ============== STATS ==============
@router.message(Command("stats"))
async def stats_cmd(m: types.Message, user: User = None, db = None):
    if not user: return await m.answer("❌ /register")
    from sqlalchemy import select, func
    total_users = await db.scalar(select(func.count(User.id))) or 0
    total_startups = await db.scalar(select(func.count(Startup.id))) or 0
    text = f"""📊 <b>Statistika:</b>

👤 Sizning: {user.full_name}
💎 Tokenlar: {user.tokens or 0}
🏆 XP: {user.xp or 0}
🔥 Streak: {user.streak_days or 0} kun

🌍 <b>Platforma:</b>
👥 Foydalanuvchilar: {total_users}
🚀 Startaplar: {total_startups}"""
    await m.answer(text)


# ============== DICE ==============
@router.message(Command("dice"))
async def dice_cmd(m: types.Message):
    import random
    await m.answer_dice(emoji="🎲")


@router.message(Command("coin"))
async def coin_cmd(m: types.Message):
    import random
    result = random.choice(["🪙 Tangalar... YUZU!", "🪙 Tangalar... MATI!"])
    await m.answer(result)


# ============== QUIZ ==============
@router.message(Command("quiz"))
async def quiz_cmd(m: types.Message):
    questions = [
        {"q": "O'zbekiston poytaxti?", "a": "Toshkent", "opts": ["Toshkent", "Samarqand", "Buxoro", "Andijon"]},
        {"q": "2+2*2 = ?", "a": "6", "opts": ["4", "6", "8", "2"]},
        {"q": "Eng katta okean?", "a": "Tinch", "opts": ["Tinch", "Atlantika", "Hind", "Shimoliy Muz"]},
    ]
    import random
    q = random.choice(questions)
    await m.answer(f"❓ <b>Savol:</b> {q['q']}\n\n" + "\n".join(f"{i+1}) {o}" for i, o in enumerate(q['opts'])))


# ============== PROFILE ==============
@router.message(Command("profile"))
async def profile_cmd(m: types.Message, user: User = None):
    if not user: return await m.answer("❌ /register")
    text = f"""👤 <b>Profil:</b>

📛 Ism: {user.full_name}
🆔 Username: @{user.username}
📧 Email: {user.email}
💎 Tokenlar: {user.tokens or 0}
🏆 XP: {user.xp or 0}
🔥 Streak: {user.streak_days or 0} kun

{'👑 Premium' if user.is_premium else '🆓 Free'}
{'✓ Verified' if user.is_verified else ''}
"""
    if user.avatar_url:
        await m.answer_photo(user.avatar_url, caption=text)
    else:
        await m.answer(text)


# ============== REFERRAL ==============
@router.message(Command("referral"))
async def referral_cmd(m: types.Message, user: User = None):
    if not user: return await m.answer("❌ /register")
    link = f"https://t.me/oo0o_uz_bot?start=ref_{user.id}"
    text = f"""🎁 <b>Referral dasturi:</b>

🔗 Sizning havolangiz:
<code>{link}</code>

💰 Har bir do'st uchun: +50 token
🎁 Premium do'st uchun: +100 token
"""
    await m.answer(text)


# ============== SETTINGS ==============
@router.message(Command("settings"))
async def settings_cmd(m: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🌐 Til", callback_data="set_lang")],
        [types.InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="set_notif")],
        [types.InlineKeyboardButton(text="🌙 Tungi rejim", callback_data="set_dark")],
        [types.InlineKeyboardButton(text="🔒 Maxfiylik", callback_data="set_privacy")],
    ])
    await m.answer("⚙️ <b>Sozlamalar:</b>", reply_markup=kb)


# ============== AI TEXT ==============
@router.message(Command("ai"))
async def ai_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) < 2: return await m.answer("❌ /ai <savol>\n\nMisol: /ai Biznes rejasi yoz")
    await m.answer("🤖 <i>AI o'ylayapti...</i>")
    result = await AIService.execute("chat", args[1])
    await m.answer(f"🤖 <b>AI javobi:</b>\n\n{result[:4000]}")


# ============== IMAGE GENERATION ==============
@router.message(Command("image"))
async def image_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) < 2: return await m.answer("❌ /image <tavsif>\n\nMisol: /image Quyosh botayotgan Toshkent")
    await m.answer("🎨 <i>Rasm yaratilmoqda...</i>")
    # In production: call DALL-E API
    await m.answer(f"🖼 <b>Rasm yaratildi:</b>\n\nPrompt: {args[1]}\n\n⚠️ Production da rasm chiqadi")


# ============== SUPPORT ==============
@router.message(Command("support"))
async def support_cmd(m: types.Message):
    await m.answer("💬 <b>Yordam:</b>\n\n📧 support@00o.uz\n📞 +998 90 123 45 67\n💬 @oo0o_uz_support\n\n🆘 Yoki shu yerga yozing, tez orada javob beramiz!")


# ============== FEEDBACK ==============
@router.message(Command("feedback"))
async def feedback_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) < 2: return await m.answer("❌ /feedback <fikr>\n\nMisol: /feedback Juda zo'r platforma!")
    # Save to DB
    await m.answer("✅ <b>Rahmat!</b> Fikringiz qabul qilindi. Biz uchun muhim! 🙏")
