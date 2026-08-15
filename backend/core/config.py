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
    # LLM & OpenRouter / Anthropic
    # ==========================================================

    OPENROUTER_API_KEY: str = Field(default="")
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    ANTHROPIC_API_KEY: str = Field(default="")
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

ENABLE_SEMANTIC_DETECTION: bool = False