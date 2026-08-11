"""
Vercel serverless entrypoint.
Wraps FastAPI app via Mangum-style adapter (raw ASGI handler for Vercel).

Vercel automatically routes all requests to /api/index.py
and passes them through this handler.
"""

import sys
import os
from pathlib import Path

# Make backend importable
ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

# Load .env if present
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# Lazy import the FastAPI app
try:
    from backend.app.main import app
    application = app
except Exception as e:
    import logging
    logging.exception("Failed to import FastAPI app: %s", e)

    # Fallback: minimal app so Vercel doesn't 500
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    application = FastAPI(title="00o.uz API (fallback)")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/")
    async def root():
        return {"ok": True, "service": "00o.uz", "mode": "vercel", "error": str(e)}

    @application.get("/api/health")
    async def health():
        return {"status": "degraded", "error": str(e)}


# Raw ASGI handler for Vercel Python runtime
def handler(request, context):
    """Vercel Python serverless function entrypoint.
    Vercel routes the raw ASGI protocol to this function.
    """
    # Vercel uses standard ASGI invocation through this contract
    from mangum import Mangum
    return Mangum(application, lifespan="off")(request, context)
