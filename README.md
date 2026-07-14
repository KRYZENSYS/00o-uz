# 🚀 00o.uz – AI Startup & Freelancer Hub

> **Uzbekistan's largest platform** combining Startup Hub + Freelancer Marketplace + AI Assistant + Investor Platform + Team Builder

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org)
[![GroqCloud](https://img.shields.io/badge/GroqCloud-AI-orange.svg)](https://groq.com)
[![i18n](https://img.shields.io/badge/i18n-UZ%20%7C%20RU%20%7C%20EN-green.svg)]()

## ✨ Features

### 🎯 Core Modules
- 🏢 **Startup Hub** - Create, showcase, and fund startups
- 👨‍💻 **Freelancer Marketplace** - Buy & sell services
- 💰 **Investor Platform** - Connect startups with investors
- 💼 **Jobs Board** - Find jobs or hire talent
- 👥 **Team Builder** - Find co-founders and team members
- 🤖 **AI Assistant** - 30+ AI tools powered by GroqCloud

### 🌐 Multi-Language
- 🇺🇿 Uzbek (default)
- 🇷🇺 Russian
- 🇬🇧 English
- Auto-detection + Manual switching
- SEO-optimized per language

### 🤖 AI (GroqCloud)
- Llama 3.3 70B
- DeepSeek R1
- Qwen 2.5
- Streaming responses
- Chat history
- File/PDF/Image analysis

## 🛠 Tech Stack

**Frontend:** Next.js 15 (App Router) · React · TypeScript · Tailwind CSS · shadcn/ui · Framer Motion · React Query · Zustand

**Backend:** FastAPI · PostgreSQL · SQLAlchemy · Redis · WebSocket · JWT

**Storage:** Cloudinary / S3

**AI:** GroqCloud (OpenAI-compatible)

**Auth:** Telegram · Google · Email+Password · OTP · 2FA

## 👨‍💻 Administrator

| Contact | Info |
|---------|------|
| 👤 **Name** | Firdavs (FirdavsVIP) |
| 📧 **Email** | f91186645@gmail.com |
| 💻 **GitHub** | https://github.com/KRYZENSYS/ |
| 📱 **Telegram** | [@FirdavsVIP](https://t.me/FirdavsVIP) |
| 🏢 **Organization** | KRYZENSYS |
| 🌐 **Website** | https://00o.uz |

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/KRYZENSYS/00o-uz.git
cd 00o-uz

# Install
npm install
cd backend && pip install -r requirements.txt && cd ..

# Setup
cp .env.example .env.local
cp backend/.env.example backend/.env

# Run
npm run dev          # Frontend (port 3000)
cd backend && uvicorn main:app --reload   # Backend (port 8000)
```

## 📁 Project Structure

```
00o-uz/
├── frontend/              # Next.js 15 App Router
│   ├── app/              # Routes
│   │   ├── [locale]/     # i18n routes (uz, ru, en)
│   │   ├── admin/        # Admin panel
│   │   └── api/          # API routes
│   ├── components/       # Reusable UI
│   ├── lib/              # Utilities
│   ├── hooks/            # React hooks
│   ├── stores/           # Zustand stores
│   ├── messages/         # i18n translations
│   └── public/           # Static files
├── backend/              # FastAPI
│   ├── app/
│   │   ├── api/          # Endpoints
│   │   ├── core/         # Config
│   │   ├── models/       # SQLAlchemy
│   │   ├── schemas/      # Pydantic
│   │   ├── services/     # Business logic
│   │   └── ai/           # GroqCloud integration
│   └── alembic/          # Migrations
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 📞 Support

- 📧 f91186645@gmail.com
- 💻 https://github.com/KRYZENSYS/
- 📱 https://t.me/FirdavsVIP

---

**Made with ❤️ by FirdavsVIP @ KRYZENSYS** 🛡️
