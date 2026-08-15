"""
Main FastAPI application for Adversarial AI Firewall.
"""

from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api.routes.health import router as health_router
from backend.api.routes.scan import router as scan_router
from backend.api.routes.metrics import router as metrics_router

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR.parent / "public"

app = FastAPI(
    title="AdAIPS",
    description="Production-grade LLM Gateway & Firewall for detecting adversarial prompt attacks.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Direct routes (root level: /scan, /health, /metrics)
app.include_router(health_router)
app.include_router(scan_router)
app.include_router(metrics_router)

# API routes (/api/scan, /api/health, /api/metrics)
app.include_router(health_router, prefix="/api")
app.include_router(scan_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")

# Versioned API routes (/api/v1/scan, /api/v1/health, /api/v1/metrics)
app.include_router(health_router, prefix="/api/v1")
app.include_router(scan_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")

# Mount static files directory (check backend/static then public/static)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
elif (PUBLIC_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR / "static")), name="static")


@app.get("/", include_in_schema=False)
async def serve_dashboard():
    """
    Serve the interactive web dashboard.
    """
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists() and (PUBLIC_DIR / "index.html").exists():
        index_file = PUBLIC_DIR / "index.html"

    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "message": "Adversarial AI Firewall API",
        "docs": "/docs",
        "health": "/health",
        "scan": "/scan",
    }