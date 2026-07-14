"""Telegram Bot"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode
import httpx

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "your_telegram_bot_token"
WEBAPP_URL = "https://00o.uz"
API_URL = "http://localhost:8000"

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


def kb_main():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 00o.uz ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="🤖 AI Yordamchi", callback_data="ai")],
        [InlineKeyboardButton(text="🚀 Startaplar", web_app=WebAppInfo(url=f"{WEBAPP_URL}/startups")), InlineKeyboardButton(text="💼 Ishlar", web_app=WebAppInfo(url=f"{WEBAPP_URL}/jobs"))],
        [InlineKeyboardButton(text="🛠️ Xizmatlar", web_app=WebAppInfo(url=f"{WEBAPP_URL}/services")), InlineKeyboardButton(text="💎 Premium", callback_data="premium")],
        [InlineKeyboardButton(text="👤 Profil", callback_data="profile"), InlineKeyboardButton(text="🎁 Referral", callback_data="referral")],
    ])


def kb_ai():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💼 Biznes reja", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai?tool=business-plan"))],
        [InlineKeyboardButton(text="💡 G'oyalar", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai?tool=startup-ideas"))],
        [InlineKeyboardButton(text="💻 Kod", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai?tool=code"))],
        [InlineKeyboardButton(text="📄 Resume", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai?tool=resume"))],
        [InlineKeyboardButton(text="🌍 Tarjimon", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai?tool=translate"))],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")],
    ])


@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    await m.answer(
        f"👋 Salom, <b>{m.from_user.first_name}</b>!\n\n"
        f"🇺🇿 <b>00o.uz</b> — O'zbekistondagi eng katta AI platforma\n\n"
        f"🤖 30+ AI vosita\n🚀 Startaplar\n💼 Ish o'rinlari\n🛠️ Freelance xizmatlar",
        reply_markup=kb_main()
    )


@dp.message(Command("ai"))
async def cmd_ai(m: types.Message):
    await m.answer("🤖 AI vosita tanlang:", reply_markup=kb_ai())


@dp.message(Command("startup"))
async def cmd_startup(m: types.Message):
    await m.answer("🚀 Startaplar", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ochish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/startups"))]]))


@dp.message(Command("jobs"))
async def cmd_jobs(m: types.Message):
    await m.answer("💼 Ish o'rinlari", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ochish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/jobs"))]]))


@dp.message(Command("premium"))
async def cmd_premium(m: types.Message):
    await m.answer(
        "💎 <b>Premium tariflar:</b>\n\n"
        "1️⃣ 1 oy — 49,000 so'm\n"
        "2️⃣ 1 yil — 490,000 so'm (-20%)\n"
        "3️⃣ Umrbod — 1,999,000 so'm\n\n"
        "✅ Limitsiz AI\n✅ Featured\n✅ Verified\n✅ Reklama yo'q",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Premium olish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/premium"))],
            [InlineKeyboardButton(text="🔙", callback_data="back_main")]
        ])
    )


@dp.message(Command("referral"))
async def cmd_referral(m: types.Message):
    link = f"https://t.me/oo0o_uz_bot?start=ref_{m.from_user.id}"
    await m.answer(
        f"🎁 <b>Referral dasturi</b>\n\nDo'stlaringizni taklif qiling va token oling!\n\n🔗 Sizning havolangiz:\n<code>{link}</code>\n\nHar bir do'st uchun: +50 token"
    )


@dp.message(Command("help"))
async def cmd_help(m: types.Message):
    await m.answer(
        "📚 <b>Buyruqlar:</b>\n\n/start — Boshlash\n/ai — AI yordamchi\n/startup — Startaplar\n/jobs — Ish o'rinlari\n/services — Xizmatlar\n/premium — Premium\n/referral — Referral\n/help — Yordam",
        reply_markup=kb_main()
    )


@dp.callback_query(F.data == "ai")
async def cb_ai(c: types.CallbackQuery):
    await c.message.edit_text("🤖 AI vosita tanlang:", reply_markup=kb_ai())


@dp.callback_query(F.data == "back_main")
async def cb_back(c: types.CallbackQuery):
    await c.message.edit_text("🏠 Asosiy menyu:", reply_markup=kb_main())


@dp.callback_query(F.data == "premium")
async def cb_premium(c: types.CallbackQuery):
    await c.message.edit_text("💎 <b>Premium:</b>\n\n1 oy: 49,000 so'm\n1 yil: 490,000 so'm\nUmrbod: 1,999,000 so'm",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💎 Olish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/premium"))], [InlineKeyboardButton(text="🔙", callback_data="back_main")]]))


@dp.callback_query(F.data == "profile")
async def cb_profile(c: types.CallbackQuery):
    await c.message.edit_text("👤 Profilingiz:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ochish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/profile"))], [InlineKeyboardButton(text="🔙", callback_data="back_main")]]))


@dp.callback_query(F.data == "referral")
async def cb_referral(c: types.CallbackQuery):
    link = f"https://t.me/oo0o_uz_bot?start=ref_{c.from_user.id}"
    await c.message.edit_text(f"🎁 <b>Referral:</b>\n\n<code>{link}</code>", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙", callback_data="back_main")]]))


async def main():
    logging.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
