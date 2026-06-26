"""
Main FastAPI application.
"""

from fastapi import FastAPI

from backend.api.routes.health import router as health_router
from backend.api.routes.scan import router as scan_router

app = FastAPI(
    title="Adversarial AI Firewall",
    description="Production-grade LLM Firewall for detecting adversarial prompts.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(scan_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Adversarial AI Firewall",
        "docs": "/docs",
    }