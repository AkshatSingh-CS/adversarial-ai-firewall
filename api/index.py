"""
Vercel Serverless Function Entry Point for AdAIPS.

This file exports the FastAPI ASGI application instance (`app`)
so Vercel's Python runtime can route HTTP requests directly into FastAPI.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path to enable backend.* imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import Request
from backend.api.main import app


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"], include_in_schema=False)
async def catch_all(request: Request, full_path: str):
    return {
        "catch_all_path": full_path,
        "url_path": request.url.path,
        "scope_path": request.scope.get("path"),
        "headers": dict(request.headers),
        "method": request.method,
    }

