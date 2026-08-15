"""
Request models for the Adversarial AI Firewall.

This module defines all request schemas used by the API.
"""

# ============================================================
# Imports
# ============================================================

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.core.config import get_settings

# ============================================================
# BaseRequest
# ============================================================

settings = get_settings()


class BaseRequest(BaseModel):
    """
    Base request model shared by all incoming API requests.

    This model contains metadata used for auditing,
    tracing, monitoring, and multi-tenant support.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    request_id: UUID = Field(
        default_factory=uuid4,
        description="Unique request identifier."
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the request was created."
    )

    tenant_id: str | None = Field(
        default=None,
        max_length=100,
        description="Optional tenant identifier."
    )

    session_id: str | None = Field(
        default=None,
        max_length=100,
        description="Optional conversation session identifier."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional client metadata."
    )

# ============================================================
# ScanRequest
# ============================================================

class ScanRequest(BaseRequest):
    """
    Request model for scanning a single prompt.

    This model represents the primary API contract used by the AI Firewall.
    Every incoming prompt is validated here before entering the detection
    pipeline.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_PROMPT_LENGTH,
        description="Prompt text submitted for security analysis."
    )

    language: str = Field(
        default="en",
        min_length=2,
        max_length=10,
        description="Language code of the submitted prompt."
    )

    target_model: str | None = Field(
        default=settings.NVIDIA_MODEL,
        max_length=100,
        description="Target LLM that will receive the prompt after scanning."
    )

    source: Literal[
        "api",
        "web",
        "sdk",
        "cli",
        "internal"
    ] = Field(
        default="api",
        description="Origin of the request."
    )

    scan_context: Literal[
        "chat",
        "rag",
        "agent",
        "document",
        "evaluation"
    ] = Field(
        default="chat",
        description="Context in which the prompt will be used."
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        """
        Validate and normalize the submitted prompt.
        """

        value = value.strip()

        if not value:
            raise ValueError("Prompt cannot be empty.")

        return value

# ============================================================
# BatchScanRequest
# ============================================================

class BatchScanRequest(BaseRequest):
    """
    Request model for scanning multiple prompts in a single request.

    This model allows clients to submit a batch of ScanRequest
    objects for efficient processing.
    """

    requests: Annotated[
        list[ScanRequest],
        Field(
            min_length=1,
            max_length=100,
            description="List of scan requests."
        ),
    ]

    @field_validator("requests")
    @classmethod
    def validate_requests(cls, value: list[ScanRequest]) -> list[ScanRequest]:
        """
        Ensure that the batch contains at least one request.
        """

        if not value:
            raise ValueError("Batch must contain at least one ScanRequest.")

        return value
