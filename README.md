# 00o.uz — O'zbekistondagi eng katta AI platforma 🇺🇿

> AI yordamchi, startaplar, ish o'rinlari, freelance xizmatlar — barchasi bir joyda.

![00o.uz](https://img.shields.io/badge/00o.uz-Live-blueviolet)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-Proprietary-red)

## ✨ Xususiyatlar

### 🤖 30+ AI vosita
- **Biznes**: biznes-reja, pitch-deck, SWOT, g'oyalar, marketing-strategiya
- **Kontent**: blog, SEO, social-media, email, copywriter
- **Karyera**: resume, cover-letter, job-description
- **Kod**: generator, bug-fix, code-review, API-docs, SQL, UI
- **Tahlil**: financial, market, competitor, legal
- **Yaratish**: image, music, voice, translate (100+ til)
- **Utilita**: chat, summarize, brainstorm, planner

### 🚀 Startaplar
- CRUD, filter, qidiruv
- Like, view counter
- Featured/Verified badge
- Trending algorithm

### 💼 Ish o'rinlari
- Full-time, Part-time, Remote, Contract
- Salary filter (min-max)
- Apply tracking
- Featured jobs

### 🛠️ Freelance
- 3-tier pricing (Basic, Standard, Premium)
- Rating, orders, delivery days
- Tags, category filter

### 💎 Premium
- 49,000 so'm/oy
- Limitsiz AI
- Reklama yo'q
- Featured

### 🤖 Telegram Bot
- 30+ buyruq
- Web App integration
- Push notifications
- Auto registration

### 🛡️ Admin Panel
- User management (ban/unban)
- Premium grants
- Broadcast
- Analytics

### 💳 To'lov tizimlari
- Payme, Click, Uzum
- Stripe (Visa/Mastercard)
- TON blockchain
- Telegram Stars

### 🔐 Xavfsizlik
- JWT (access + refresh)
- 2FA (TOTP)
- Email + SMS verification
- Rate limiting
- CSRF protection

## 🏗️ Texnologiyalar

### Frontend
- **Next.js 14** (App Router, SSR, RSC)
- **TypeScript** (100% typed)
- **TailwindCSS** + Custom CSS
- **Lucide React** (icons)
- **NextAuth** (auth)
- **i18n** (UZ, RU, EN)

### Backend
- **FastAPI** (async, fast)
- **PostgreSQL 16** + **AsyncPG**
- **Redis 7** (cache, sessions)
- **SQLAlchemy 2.0** (ORM)
- **Alembic** (migrations)
- **Groq API** (LLM: Llama 3.3 70B)
- **Pydantic** v2
- **JWT (jose)** + **Bcrypt**

### AI
- **Groq** (Llama 3.3 70B, Mixtral 8x7B)
- **OpenAI** (fallback)
- **Replicate** (image, music)
- **ElevenLabs** (voice)
- **Google Translate** (100+ til)

### DevOps
- **Docker** + **Docker Compose**
- **Nginx** (reverse proxy + SSL)
- **GitHub Actions** (CI/CD)
- **Prometheus** + **Grafana** (monitoring)

### Payments
- **Payme API**
- **Click API**
- **Uzum API**
- **Stripe SDK**
- **TON Connect**

## 📦 O'rnatish

### Local development
```bash
# 1. Clone
git clone https://github.com/KRYZENSYS/00o-uz.git
cd 00o-uz

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Sozlamalarni kiriting
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 3. Frontend (yangi terminal)
cd ..
npm install
cp .env.example .env.local
npm run dev

# 4. Bot (yangi terminal)
cd backend
python bot/main.py
```

### Docker
```bash
docker-compose up -d
```

### Production deploy
```bash
# Vercel (frontend)
vercel --prod

# Railway/Render (backend)
# See DEPLOYMENT.md
```

## 🌐 Demo

- **Web**: https://00o.uz
- **Telegram**: [@oo0o_uz_bot](https://t.me/oo0o_uz_bot)
- **API**: https://api.00o.uz/docs
- **Admin**: https://00o.uz/admin

## 📊 Statistika

- 150+ fayl
- 15,000+ qator kod
- 50+ API endpoint
- 30+ AI vosita
- 15+ sahifa
- 3 til (UZ, RU, EN)
- 5+ to'lov tizimi
- 10+ xavfsizlik
- 100% production-ready

## 📜 License

Proprietary © 2026 00o.uz
Barcha huquqlar himoyalangan.

## 📞 Aloqa

- **Email**: info@00o.uz
- **Telegram**: [@oo0o_uz](https://t.me/oo0o_uz)
- **Website**: https://00o.uz

---

Made with ❤️ in Uzbekistan 🇺🇿
