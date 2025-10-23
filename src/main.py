"""Minimal entry point for agentic scraping prototype."""
from __future__ import annotations

import argparse

from .config import load_azure_openai_client
from .ai import extract_product_snapshot
from .scraper import fetch_page, extract_visible_text


def scrape_and_analyze(url: str, out_path: str | None = None) -> str:
    """Fetch a page, extract text, and analyze with LLM to produce product snapshot.
    
    Args:
        url: Target URL to scrape
        out_path: Optional file path to write JSON output
        
    Returns:
        JSON string of ProductSnapshot
    """
    client, deployment = load_azure_openai_client()
    html = fetch_page(url)
    page_text = extract_visible_text(html)
    result = extract_product_snapshot(client, deployment, url, page_text)
    
    payload = result.model_dump_json(indent=2, ensure_ascii=False)
    
    if out_path:
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(payload)
    
    return payload


def cli() -> None:
    """Parse command-line arguments and execute scraping workflow."""
    parser = argparse.ArgumentParser(description="Agentic product scraper")
    parser.add_argument("url", help="Target URL to scrape")
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional path to write JSON output",
    )
    args = parser.parse_args()
    result = scrape_and_analyze(args.url, args.out)
    print(result)


if __name__ == "__main__":
    cli()
