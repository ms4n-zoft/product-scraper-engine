"""Logging configuration for the scraper engine."""
from loguru import logger
import sys


def configure_logging(level: str = "DEBUG", log_file: str | None = None) -> None:
    """Configure loguru logging with sensible defaults."""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )
    
    # Add file handler if specified
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation="500 MB",
            retention="7 days"
        )


# Configure on import
configure_logging()
