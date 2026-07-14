# 🚀 00o.uz — O'zbekistondagi eng katta AI platforma

> **300+ funksiyali, to'liq ishlab chiqarishga tayyor professional web va bot platforma**

## ✨ Asosiy xususiyatlar

### 🤖 AI (30+ vosita)
- Chat, Business Plan, Pitch Deck, Resume, Cover Letter
- Code Generation, Bug Fix, SQL, UI Components
- Marketing, SEO, Blog, Email
- Translator (100+ til), Summarizer, Brainstorm
- AI Image, Logo, Avatar, Thumbnail, Video, Voice

### 🏢 Platformalar
- **Startaplar** — boshlovchilar uchun
- **Ish o'rinlari** — vakansiyalar va rezyume
- **Xizmatlar** — freelance marketplace
- **Kurslar** — video ta'lim platformasi
- **Investorlar** — sarmoya izlash
- **Jamoalar** — co-founder topish
- **Market** — e-commerce marketplace
- **Events** — tadbirlar va uchrashuvlar

### 💬 Communication
- Real-time chat (WebSocket)
- Voice/Video calls (WebRTC)
- Group calls (50+ odam)
- Screen sharing
- File sharing (50MB)
- Live streaming + donations

### 🎮 Gamification
- 10 ta level, 15+ badge
- Daily missions, Streak
- XP, Leaderboard
- Achievements system

### 🔐 Security
- Email/Phone verification
- KYC (Passport, ID)
- 2FA (Google Authenticator)
- Biometric login (WebAuthn)
- Device management
- Login history
- Block/Report users

### 💳 To'lov
- Payme, Click, Uzum, Stripe
- TON, Crypto (tez kunda)
- 3 ta Premium tarif
- Token tizimi
- Referral dasturi
- Coupon codes

### 🌐 Integrations (40+)
- Google (Drive, Calendar, Sheets, Meet, Analytics)
- Slack, Discord, Telegram, Zoom
- GitHub, GitLab, Jira, Linear
- Stripe, Mailchimp, SendGrid, Twilio
- Webhooks, API keys, OAuth 2.0

### 📊 Admin Panel
- Dashboard, Analytics, Charts
- User management (ban, role, verify)
- Content moderation (AI)
- Broadcast, Push notifications
- Email campaigns
- Coupons, Coupons, Landing pages
- System logs, Health check

### 🤖 Telegram Bot (60+ buyruq)
- Asosiy: /start, /help, /profile
- AI: /ai, /image, /translate, /code
- Utility: /qr, /currency, /weather, /prayer, /calc
- Fun: /dice, /coin, /quiz, /leaderboard
- Business: /stats, /achievements, /daily

### 🎨 Frontend
- 30+ sahifa (Next.js 14, App Router)
- 3 til (UZ, RU, EN) — i18n
- Glassmorphism design
- PWA, SEO, Mobile-first
- Dark mode
- Real-time WebSocket

## 🛠 Texnologiyalar

**Backend:**
- FastAPI (async)
- SQLAlchemy 2.0 + PostgreSQL
- Redis, WebSocket, WebRTC
- JWT, OAuth 2.0
- OpenAI, DALL-E 3, Whisper

**Frontend:**
- Next.js 14 (App Router)
- TypeScript, Tailwind CSS
- Lucide icons, Framer Motion
- i18next, PWA

**Bot:**
- aiogram 3
- PostgreSQL + Redis
- Webhook + Polling

**DevOps:**
- Docker, Docker Compose
- Nginx, SSL
- GitHub Actions CI/CD
- Sentry, Prometheus, Grafana

## 📁 Struktura

```
00o-uz/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/v1/  # 20+ API moduli
│   │   ├── core/    # Config, DB, Security
│   │   ├── models/  # 50+ SQLAlchemy model
│   │   ├── services/ # AI, Payment, Email, Bot
│   │   ├── ai/      # 30+ AI tool
│   │   └── main.py
│   ├── tests/       # pytest
│   └── requirements.txt
├── src/             # Next.js frontend
│   ├── app/[locale] # 30+ sahifa
│   ├── components/  # Reusable components
│   ├── i18n/        # Translations
│   └── lib/         # Utils, API client
├── bot/             # Telegram bot
│   ├── handlers/    # 60+ buyruq
│   ├── services/    # AI, DB
│   └── main.py
└── docker-compose.yml
```

## 🚀 Ishga tushirish

### Docker
```bash
docker-compose up -d
```

### Manual

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
npm install
npm run dev  # http://localhost:3000
```

**Bot:**
```bash
cd bot
pip install -r requirements.txt
python main.py
```

## 📊 Statistika

- **Backend:** 70+ API endpoint
- **Models:** 50+ jadval
- **Frontend:** 30+ sahifa
- **Bot:** 60+ buyruq
- **AI Tools:** 30+ vosita
- **Integrations:** 40+ service
- **Languages:** 3+ (UZ, RU, EN)
- **Jami fayllar:** 300+

## 🌐 Demo

- **Web:** [https://00o.uz](https://00o.uz)
- **Bot:** [@oo0o_uz_bot](https://t.me/oo0o_uz_bot)
- **API Docs:** [https://api.00o.uz/docs](https://api.00o.uz/docs)

## 📝 License

MIT

## 👥 Team

**KRYZENSYS** — [github.com/KRYZENSYS](https://github.com/KRYZENSYS)

---

⭐️ Agar yoqsa, star bering!
