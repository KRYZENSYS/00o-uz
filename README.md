# 🚀 00o.uz - AI Startup & Freelancer Hub

> **O'zbekistondagi eng katta AI-powered startup, frilanser va investor platformasi**

## ✨ Xususiyatlar

### 🤖 AI Yordamchi (GroqCloud)
30+ vosita: Chat, Business Plan, Pitch Deck, Startup Analyzer, Code Generator, Translator, Summarizer, SEO, Marketing, Resume Builder va boshqalar

### 🎯 Asosiy modullar
- 🚀 Startaplar (CRUD, investitsiya)
- 💼 Frilanser xizmatlar (Basic/Standard/Premium)
- 💼 Ish o'rinlari
- 💰 Investorlar
- 👥 Jamoalar
- 💬 Xabarlar (WebSocket)
- 🛡️ Admin panel

### 🌍 i18n
3 til: 🇺🇿 O'zbek, 🇷🇺 Русский, 🇬🇧 English

## 🏗️ Texnologiyalar

**Frontend:** Next.js 15 · TypeScript · Tailwind CSS · next-intl
**Backend:** FastAPI · SQLAlchemy 2.0 (async) · PostgreSQL · Redis · JWT · GroqCloud AI
**Auth:** Email, Telegram, Google OAuth, 2FA, OTP
**Deployment:** Vercel · Railway · Docker

## 📁 Struktura

```
00o-uz/
├── src/                     # Next.js frontend
│   ├── app/[locale]/        # i18n routes
│   │   ├── page.tsx         # Landing
│   │   ├── login/           # Auth
│   │   ├── register/
│   │   ├── dashboard/
│   │   ├── ai/              # AI Assistant
│   │   └── startups/        # CRUD
│   ├── components/          # React components
│   ├── i18n/                # Config
│   └── messages/            # uz, ru, en
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── core/            # config, db, security
│   │   ├── models/          # SQLAlchemy
│   │   ├── ai/              # GroqCloud
│   │   └── api/v1/          # endpoints
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## 🚀 Tezkor boshlash

### Frontend
```bash
npm install
cp .env.example .env.local
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 👨‍💻 Admin
**Email:** `f91186645@gmail.com`
**Telegram:** [@FirdavsVIP](https://t.me/FirdavsVIP)
**Company:** KRYZENSYS

## 📜 License
MIT © 2026 00o.uz

**Made with ❤️ by KRYZENSYS**
