"""Environment variable utilities."""
from __future__ import annotations

import os


def get_required_env_var(name: str) -> str:
    """Retrieve a required environment variable or raise an error.
    
    Args:
        name: Environment variable name
        
    Returns:
        Environment variable value
        
    Raises:
        RuntimeError: If the environment variable is not set
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
