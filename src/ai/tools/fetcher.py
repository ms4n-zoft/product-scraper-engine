"""Tool for fetching and extracting text from URLs via function calling."""
from __future__ import annotations

import json
import httpx


def fetch_page_text(url: str) -> str:
    """Fetch a URL and extract visible text content."""
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL: {url}")
    
    headers = {
        "User-Agent": "product-scraper-prototype/0.1 (+https://example.com)"
    }
    
    try:
        with httpx.Client(follow_redirects=True, timeout=30.0, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text
    except httpx.HTTPError as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to fetch URL: {str(e)}"
        })
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text_chunks = [chunk.strip() for chunk in soup.stripped_strings if chunk.strip()]
    text = " \n".join(text_chunks)
    
    return json.dumps({
        "success": True,
        "url": url,
        "text": text,
        "length": len(text)
    })


def get_fetch_page_text_tool() -> dict:
    """OpenAI function calling schema for fetch_page_text."""
    return {
        "type": "function",
        "name": "fetch_page_text",
        "description": (
            "Fetch a URL and extract its visible text content. Use this when you need to get "
            "content from a webpage to complete product analysis tasks. Returns the extracted "
            "text that can be analyzed for product information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL to fetch (must start with http:// or https://)"
                }
            },
            "required": ["url"],
            "additionalProperties": False
        },
        "strict": True
    }
