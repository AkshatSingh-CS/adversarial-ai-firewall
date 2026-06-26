"""
Response models for the Adversarial AI Firewall.

This module defines all API response schemas returned by the AI Firewall.
"""

# ============================================================
# Imports
# ============================================================

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# ThreatMatch
# ============================================================

class ThreatMatch(BaseModel):
    """
    Represents a single threat detected by the AI Firewall.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    attack_type: str = Field(
        ...,
        max_length=100,
        description="Type of detected attack."
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Detection confidence between 0 and 1."
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] = Field(
        ...,
        description="Severity level assigned to the detected threat."
    )

    detection_layer: str = Field(
        ...,
        max_length=100,
        description="Detection layer responsible for identifying the threat."
    )

    description: str = Field(
        ...,
        max_length=500,
        description="Human-readable explanation of the detected threat."
    )

# ============================================================
# ScanResponse
# ============================================================

class ScanResponse(BaseModel):
    """
    Response model returned after scanning a single prompt.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    request_id: UUID = Field(
        ...,
        description="Unique identifier of the processed request."
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the scan completed."
    )

    status: Literal[
        "success",
        "failed",
    ] = Field(
        default="success",
        description="Overall processing status."
    )

    blocked: bool = Field(
        ...,
        description="Whether the prompt should be blocked."
    )

    risk_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall calculated risk score."
    )

    risk_level: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] = Field(
        ...,
        description="Overall risk classification."
    )

    threats: list[ThreatMatch] = Field(
        default_factory=list,
        description="Detected threats."
    )

    processing_time_ms: float = Field(
        ...,
        ge=0,
        description="Processing time in milliseconds."
    )

    message: str = Field(
        ...,
        max_length=500,
        description="Human-readable result summary."
    )

# ============================================================
# BatchScanResponse
# ============================================================

class BatchScanResponse(BaseModel):
    """
    Response model returned after scanning multiple prompts.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    request_id: UUID = Field(
        ...,
        description="Unique identifier for the batch request."
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when batch processing completed."
    )

    total_requests: int = Field(
        ...,
        ge=1,
        description="Total number of prompts submitted."
    )

    processed_requests: int = Field(
        ...,
        ge=0,
        description="Number of successfully processed prompts."
    )

    blocked_requests: int = Field(
        ...,
        ge=0,
        description="Number of prompts blocked by the firewall."
    )

    processing_time_ms: float = Field(
        ...,
        ge=0,
        description="Total batch processing time in milliseconds."
    )

    results: list[ScanResponse] = Field(
        default_factory=list,
        description="Scan results for each submitted prompt."
    )