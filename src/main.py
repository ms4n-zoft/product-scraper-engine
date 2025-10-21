"""Minimal entry point for agentic scraping prototype."""
from __future__ import annotations

import argparse

import httpx
from bs4 import BeautifulSoup
from openai import AzureOpenAI

from .azure_client import load_client
from .schemas import ProductSnapshot

SYSTEM_PROMPT = (
    "You are a product intelligence assistant generating data for a catalog. "
    "Always populate the ProductSnapshot schema exactly, using only evidence from the page "
    "content provided. Write in a neutral, professional tone, keep numeric values as numbers, "
    "and ensure every URL is an https link. If information is unavailable, return nulls "
    "or empty lists as appropriate."
)


def fetch_page(url: str) -> str:
    """Retrieve raw HTML for the target URL."""
    headers = {
        "User-Agent": "product-scraper-prototype/0.1 (+https://example.com)"
    }
    with httpx.Client(follow_redirects=True, timeout=30.0, headers=headers) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def extract_visible_text(html: str) -> str:
    """Strip non-text elements and condense whitespace for LLM consumption."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text_chunks = [chunk.strip() for chunk in soup.stripped_strings if chunk.strip()]
    text = " \n".join(text_chunks)
    return text


def analyze_page(
    client: AzureOpenAI,
    deployment: str,
    url: str,
    page_text: str,
) -> ProductSnapshot:
    """Map page text into the ProductSnapshot schema via Azure OpenAI."""
    user_prompt = (
        "Use the webpage content to complete the ProductSnapshot schema. "
        "Stay faithful to verified details, prefer official data, and do not fabricate. "
        "If a field is unknown, return null."
        f"\n\nURL: {url}\n\nWebpage content:\n{page_text}"
    )
    completion = client.beta.chat.completions.parse(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=ProductSnapshot,
    )
    return completion.choices[0].message.parsed


def run(url: str, show_raw: bool, test_mode: bool, out_path: str | None) -> None:
    print(f"[info] loading Azure OpenAI client ...")
    client, deployment = load_client()

    print(f"[info] fetching page: {url}")
    html = fetch_page(url)

    print("[info] extracting visible text")
    page_text = extract_visible_text(html)

    print("\n--- page_text ---")
    print(page_text)
    print("--- end page_text ---\n")

    if test_mode:
        response = input("Proceed to LLM analysis? (y/n): ").strip().lower()
        if response != "y":
            print("[info] test mode: skipping LLM analysis")
            return

    print("[info] sending content to LLM")
    result = analyze_page(client, deployment, url, page_text)

    if show_raw:
        print("\n--- LLM response ---")
        print(result.model_dump_json(indent=2, ensure_ascii=False))
        print("--- end LLM response ---\n")

    payload = result.model_dump_json(indent=2, ensure_ascii=False)
    print(payload)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(payload)


def cli() -> None:
    parser = argparse.ArgumentParser(description="Minimal agentic scraper prototype")
    parser.add_argument("url", help="Target URL to scrape")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Echo the LLM response in full detail",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: display extracted text and prompt for confirmation before calling LLM",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="Optional path to write the JSON result",
    )
    args = parser.parse_args()
    run(args.url, args.raw, args.test, args.out)


if __name__ == "__main__":
    cli()
