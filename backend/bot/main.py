"""Telegram Bot - 30+ commands"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://00o.uz")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🚀 Ochish 00o.uz", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🤖 AI Chat", callback_data="ai_chat"), InlineKeyboardButton("💼 Profil", callback_data="profile")],
        [InlineKeyboardButton("🚀 Startup", callback_data="startup"), InlineKeyboardButton("💼 Freelance", callback_data="freelance")],
        [InlineKeyboardButton("💼 Jobs", callback_data="jobs"), InlineKeyboardButton("💰 Investors", callback_data="investors")],
        [InlineKeyboardButton("🎁 Referal", callback_data="referral"), InlineKeyboardButton("💎 Premium", callback_data="premium")],
        [InlineKeyboardButton("❓ Yordam", callback_data="help")],
    ]
    await update.message.reply_text(
        f"👋 Assalomu alaykum, *{user.first_name}*!\n\n"
        f"Men *00o.uz* rasmiy botiman 🤖\n\n"
        f"🎯 Imkoniyatlar:\n• AI yordamchi (30+ vosita)\n• Startup yaratish\n• Freelance xizmatlar\n• Ish o'rinlari\n• Premium imkoniyatlar",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📚 *Buyruqlar:*
/start, /help, /profile, /ai, /startup, /jobs, /premium, /referral, /wallet
/business_plan, /pitch_deck, /code, /translate, /summarize, /image
/team, /mentor, /notifications, /settings, /language
"""
    await update.message.reply_text(text, parse_mode="Markdown")


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("✏️ Tahrirlash", web_app=WebAppInfo(url=f"{WEBAPP_URL}/settings"))]]
    await update.message.reply_text(
        f"👤 *Profil*\nIsm: {user.first_name}\nID: `{user.id}`",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


async def ai_chat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💬 AI Chat", web_app=WebAppInfo(url=f"{WEBAPP_URL}/ai"))]]
    await update.message.reply_text("🤖 *AI Yordamchi* - 30+ vosita", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def startup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 Yangi startup", web_app=WebAppInfo(url=f"{WEBAPP_URL}/startups/create"))]]
    await update.message.reply_text("🚀 *Startaplar*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def jobs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💼 Ish topish", web_app=WebAppInfo(url=f"{WEBAPP_URL}/jobs"))]]
    await update.message.reply_text("💼 *Ish o'rinlari*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💎 Premium olish", callback_data="buy_premium")]]
    await update.message.reply_text("💎 *Premium*\n49,000 so'm/oy", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def referral_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref_link = f"https://t.me/oo0o_uz_bot?start=ref_{user.id}"
    await update.message.reply_text(
        f"🎁 *Referral*\nLink: `{ref_link}`\n\n1 do'st = 50 token, 5 = Premium 1 oy",
        parse_mode="Markdown"
    )


async def wallet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 *Hamyon*\n💎 0 token | 💵 0 UZS")


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "ai_chat":
        await query.message.reply_text("🤖 https://00o.uz/ai")
    elif data == "trending_startups":
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{API_URL}/api/v1/startups/trending/list")
                items = res.json()[:5]
                text = "📈 *Trend:*\n\n" + "\n".join(f"{i+1}. *{s['name']}*" for i, s in enumerate(items))
                await query.message.reply_text(text, parse_mode="Markdown")
        except: await query.message.reply_text("❌ Xatolik")
    elif data == "buy_premium":
        await query.message.reply_text("💎 To'lov: https://00o.uz/premium")
    else:
        await query.message.reply_text("Tez orada!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(f"{API_URL}/api/v1/ai/chat", json={"input": update.message.text, "language": "uz"})
            data = res.json()
            await update.message.reply_text(f"🤖 {data.get('content', 'Xatolik')}")
    except:
        await update.message.reply_text("❌ AI xizmati vaqtincha ishlamayapti")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("ai", ai_chat_cmd))
    app.add_handler(CommandHandler("startup", startup_cmd))
    app.add_handler(CommandHandler("jobs", jobs_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(CommandHandler("referral", referral_cmd))
    app.add_handler(CommandHandler("wallet", wallet_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logger.info("Bot started!")
    app.run_polling()


if __name__ == "__main__":
    main()
