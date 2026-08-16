"""Vercel and local ASGI entrypoint for the AdAIPS FastAPI application."""

from backend.api.main import app

__all__ = ["app"]
