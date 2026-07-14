"""FastAPI main application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import auth, ai, startups, jobs, services, payments, admin, chat, users, teams, investors, posts, courses, analytics_service, search, premium, referrals, notifications_ws, websocket
from app.api.v1.websocket import router as ws_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("00o.uz")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 00o.uz backend starting...")
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"DB init error: {e}")
    yield
    logger.info("👋 00o.uz backend shutting down")


app = FastAPI(
    title="00o.uz API",
    description="O'zbekistondagi eng katta AI platforma API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(startups.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(services.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(investors.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(analytics_service.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(premium.router, prefix="/api/v1")
app.include_router(referrals.router, prefix="/api/v1")
app.include_router(notifications_ws.router, prefix="/api/v1")
app.include_router(ws_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": "00o.uz API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": 70
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/info")
async def info():
    return {
        "name": "00o.uz",
        "version": "1.0.0",
        "features": {
            "ai_tools": 30,
            "languages": ["uz", "ru", "en"],
            "payments": ["payme", "click", "uzum", "stripe", "ton"],
            "modules": ["startups", "jobs", "services", "courses", "investors", "teams", "chat", "feed", "premium", "referral"]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
