"""
Application configuration.

Centralized configuration management for the
Adversarial AI Firewall.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "AdAIPS"
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    # ==========================================================
    # Detection
    # ==========================================================

    MAX_PROMPT_LENGTH: int = 10_000

    REGEX_THRESHOLD: float = 0.30
    SEMANTIC_THRESHOLD: float = 0.70

    # ==========================================================
    # LLM providers
    # ==========================================================

    # Primary provider: NVIDIA-hosted NIM API. Vercel injects this secret
    # into the Python serverless runtime from Project Environment Variables.
    NVIDIA_API_KEY: str = Field(default="", repr=False)
    NVIDIA_MODEL: str = "nvidia/nemotron-3-ultra-550b-a55b"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MAX_TOKENS: int = 512

    # Optional fallback providers.
    OPENROUTER_API_KEY: str = Field(default="", repr=False)
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    ANTHROPIC_API_KEY: str = Field(default="", repr=False)
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    ANTHROPIC_TIMEOUT: int = 30
    LLM_TIMEOUT: int = 30

    # ==========================================================
    # Batch Processing
    # ==========================================================

    MAX_BATCH_SIZE: int = 50

    # ==========================================================
    # Pydantic Settings
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()
