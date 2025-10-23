"""Scraper engine for fetching and parsing web content."""
from .fetcher import fetch_page
from .parser import extract_visible_text

__all__ = ["fetch_page", "extract_visible_text"]
