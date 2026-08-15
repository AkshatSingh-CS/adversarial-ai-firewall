"""
Pydantic models for LLM responses.

These models validate structured outputs
returned by Claude.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LLMAnalysisResult(BaseModel):
    """
    Structured response returned by Claude.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    attack_detected: bool = Field(
        ...,
        description="Whether an attack was detected.",
    )

    attack_type: str | None = Field(
        default=None,
        max_length=100,
        description="Detected attack category.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score.",
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] | None = Field(
        default=None,
        description="Threat severity.",
    )

    reason: str = Field(
        ...,
        max_length=1000,
        description="Reason for the decision.",
    )