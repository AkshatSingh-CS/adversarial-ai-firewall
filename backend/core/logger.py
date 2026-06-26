"""
Centralized logging configuration for the Adversarial AI Firewall.

This module provides a single logger instance that can be imported
throughout the application.

Features:
- Console logging
- File logging
- Automatic log rotation
- Log retention
- Structured log formatting
"""

from pathlib import Path

from loguru import logger

from backend.core.config import settings


def setup_logger() -> None:
    """
    Configure the application logger.

    This function removes the default Loguru handler and
    configures both console and file logging.
    """

    # Remove default logger
    logger.remove()

    # Ensure logs directory exists
    log_directory = Path("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    # Console Logger
    logger.add(
        sink=lambda message: print(message, end=""),
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # File Logger
    logger.add(
        log_directory / "application.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level:<8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
    )


# Configure logger when this module is imported
setup_logger()

# Export shared logger
app_logger = logger