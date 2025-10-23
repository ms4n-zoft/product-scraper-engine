"""HTML parsing and text extraction utilities."""
from __future__ import annotations

from bs4 import BeautifulSoup


def extract_visible_text(html: str) -> str:
    """Extract and clean visible text from HTML for LLM processing.
    
    Removes script, style, noscript, and svg tags, then extracts and
    normalizes the text content with proper whitespace handling.
    
    Args:
        html: Raw HTML content
        
    Returns:
        Cleaned text content suitable for LLM analysis
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text_chunks = [chunk.strip() for chunk in soup.stripped_strings if chunk.strip()]
    text = " \n".join(text_chunks)
    return text
