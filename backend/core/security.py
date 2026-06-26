"""
Security utilities for the Adversarial AI Firewall.

This module provides helper functions used throughout the
application for validating requests, generating request IDs,
hashing prompts, and performing basic security checks.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timezone

from backend.core.config import settings


def validate_prompt_length(prompt: str) -> bool:
    """
    Validate prompt length against configured limits.

    Args:
        prompt: User submitted prompt.

    Returns:
        True if prompt length is acceptable.
    """
    return 0 < len(prompt) <= settings.MAX_PROMPT_LENGTH


def generate_request_id() -> str:
    """
    Generate a secure request identifier.

    Returns:
        Hexadecimal request id.
    """
    return secrets.token_hex(16)


def hash_prompt(prompt: str) -> str:
    """
    Generate SHA-256 hash of a prompt.

    The original prompt should never be used
    as a database identifier.

    Args:
        prompt: User prompt.

    Returns:
        SHA256 hash.
    """
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def current_timestamp() -> str:
    """
    Return current UTC timestamp.

    Returns:
        ISO8601 timestamp.
    """
    return datetime.now(timezone.utc).isoformat()


def validate_api_key(
    supplied_key: str,
    configured_key: str,
) -> bool:
    """
    Constant-time API key comparison.

    Args:
        supplied_key:
            API key from request.

        configured_key:
            Expected API key.

    Returns:
        True if keys match.
    """
    return secrets.compare_digest(
        supplied_key,
        configured_key,
    )