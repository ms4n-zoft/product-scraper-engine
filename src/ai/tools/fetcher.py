"""Tool for fetching and extracting text from URLs via function calling."""
from __future__ import annotations

import json
import httpx
from bs4 import BeautifulSoup
from loguru import logger


def fetch_page_text(url: str) -> str:
    """Fetch a URL and extract visible text content."""
    logger.debug(f"Fetching URL: {url}")
    
    if not url.startswith(("http://", "https://")):
        logger.error(f"Invalid URL format: {url}")
        raise ValueError(f"Invalid URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        with httpx.Client(follow_redirects=True, timeout=30.0, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text
            logger.debug(f"Successfully fetched {len(html)} bytes from {url}")
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {str(e)}")
        return json.dumps({
            "success": False,
            "error": f"Failed to fetch URL: {str(e)}"
        })
    
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text_chunks = [chunk.strip() for chunk in soup.stripped_strings if chunk.strip()]
    text = " \n".join(text_chunks)
    
    # Extract all href links with their text
    links = []
    for link in soup.find_all("a", href=True):
        href = link.get("href", "").strip()
        link_text = link.get_text(strip=True)
        if href and href != "#":
            links.append({
                "href": href,
                "text": link_text if link_text else "[no text]"
            })
    
    logger.info(f"Extracted {len(text)} chars and {len(links)} links from {url}")
    return json.dumps({
        "success": True,
        "url": url,
        "text": text,
        "length": len(text),
        "links": links
    })


def get_fetch_page_text_tool() -> dict:
    """OpenAI function calling schema for fetch_page_text."""
    return {
        "type": "function",
        "name": "fetch_page_text",
        "description": (
            "Fetch a URL and extract its visible text content along with all page links. "
            "Use this to retrieve content from webpages to complete product analysis tasks. "
            "Returns the extracted text content, page structure information, and a list of all "
            "links found on the page (href and link text) which helps you navigate to related pages "
            "like About, Products, Contact, or other sections to gather comprehensive information."
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
