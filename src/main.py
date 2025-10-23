"""Minimal entry point for agentic scraping prototype."""
from __future__ import annotations

import argparse

from .config import load_azure_openai_client
from .ai.agentic_analyzer import extract_product_snapshot_agentic


def scrape_and_analyze(url: str, out_path: str | None = None) -> str:
    """Analyze a product page using agentic function calling."""
    client, deployment = load_azure_openai_client()
    result = extract_product_snapshot_agentic(client, deployment, url)
    
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
