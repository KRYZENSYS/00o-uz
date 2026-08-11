"""
Vercel serverless health-check endpoint.
Returns 200 with service info. Used by uptime monitors.
"""

import json
import os
import time
from datetime import datetime, timezone


def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-store",
        },
        "body": json.dumps({
            "status": "ok",
            "service": "00o.uz",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime": time.time(),
            "env": os.getenv("VERCEL_ENV", "development"),
            "region": os.getenv("VERCEL_REGION", "unknown"),
        }),
    }
