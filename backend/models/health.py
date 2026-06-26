"""
Health models for the Adversarial AI Firewall.

This module defines response models used by health,
readiness, and liveness endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """
    Standard response model for service health endpoints.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    status: Literal[
        "healthy",
        "degraded",
        "unhealthy",
    ] = Field(
        ...,
        description="Overall health status of the service.",
    )

    service: str = Field(
        default="Adversarial AI Firewall",
        description="Service name.",
    )

    version: str = Field(
        default="0.1.0",
        description="Current application version.",
    )

    environment: str = Field(
        default="development",
        description="Current deployment environment.",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the health response was generated.",
    )

    uptime_seconds: float = Field(
        default=0.0,
        ge=0,
        description="Application uptime in seconds.",
    )

    message: str = Field(
        default="Service is operating normally.",
        max_length=500,
        description="Human-readable health message.",
    )