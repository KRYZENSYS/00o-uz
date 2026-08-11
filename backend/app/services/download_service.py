"""
Multi-platform video/media downloader service.
Supports YouTube, TikTok, Instagram, Twitter/X via yt-dlp.
"""

import logging
import os
import subprocess
import uuid
from typing import Any, Dict

logger = logging.getLogger(__name__)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/tmp/00o-downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

PLATFORMS = ["youtube", "tiktok", "instagram", "twitter", "facebook", "vimeo", "reddit", "soundcloud"]


async def download_media(url: str, format: str = "mp4", quality: str = "best") -> Dict[str, Any]:
    if not url:
        return {"error": "Empty URL"}
    file_id = str(uuid.uuid4())[:8]
    out_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--no-playlist",
        "-o", out_template,
        "-f", "best" if quality == "best" else f"{quality}[ext={format}]/{quality}/best",
        url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            return {"error": "yt-dlp failed", "stderr": proc.stderr[-500:], "url": url}
        for fname in os.listdir(DOWNLOAD_DIR):
            if fname.startswith(file_id + "."):
                fpath = os.path.join(DOWNLOAD_DIR, fname)
                size = os.path.getsize(fpath)
                return {
                    "success": True,
                    "file_id": file_id,
                    "filename": fname,
                    "path": fpath,
                    "size": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "url": url,
                    "format": fname.rsplit(".", 1)[-1] if "." in fname else "unknown",
                }
        return {"error": "File not produced", "stderr": proc.stderr[-300:]}
    except FileNotFoundError:
        return {"error": "yt-dlp not installed", "hint": "pip install yt-dlp"}
    except subprocess.TimeoutExpired:
        return {"error": "Download timeout (120s)"}
    except Exception as e:
        return {"error": str(e)}


async def get_video_info(url: str) -> Dict[str, Any]:
    try:
        cmd = ["yt-dlp", "--no-warnings", "--dump-json", "--skip-download", url]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            return {"error": "Failed to fetch info", "stderr": proc.stderr[-200:]}
        import json
        info = json.loads(proc.stdout)
        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "description": (info.get("description") or "")[:500],
            "thumbnail": info.get("thumbnail"),
            "ext": info.get("ext"),
            "platform": info.get("extractor"),
        }
    except FileNotFoundError:
        return {"error": "yt-dlp not installed"}
    except Exception as e:
        return {"error": str(e)}
