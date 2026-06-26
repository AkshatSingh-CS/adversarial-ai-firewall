"""
Application configuration.

This module provides centralized configuration management for the
Adversarial AI Firewall project.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    APP_NAME: str = "Adversarial AI Firewall"
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    MAX_PROMPT_LENGTH: int = 10000

    API_KEY: str = "change-me"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
from functools import lru_cache


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()