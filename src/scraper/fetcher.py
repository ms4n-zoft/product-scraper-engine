"""HTTP fetching utilities for web pages."""
from __future__ import annotations

import httpx


def fetch_page(url: str) -> str:
    """Fetch raw HTML content from a URL with standard headers.
    
    Args:
        url: Target URL to fetch
        
    Returns:
        Raw HTML content as string
        
    Raises:
        httpx.HTTPError: If the request fails
    """
    headers = {
        "User-Agent": "product-scraper-prototype/0.1 (+https://example.com)"
    }
    with httpx.Client(follow_redirects=True, timeout=30.0, headers=headers) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text
