# Product Scraper (Prototype)

Minimal Python prototype for experimenting with agentic scraping backed by Azure OpenAI. Given a starting URL, the script fetches the page, strips boilerplate, and asks an LLM to structure product-related insights.

## Prerequisites

- Python 3.11+
- Azure OpenAI resource with a model deployment (e.g. `gpt-5-mini`)

## Setup

1. Clone or open this repo. Optionally create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Azure OpenAI credentials (see `.env.example`). Either export the variables or copy the file to `.env` and fill in values.

## Usage

```bash
python -m src.main https://www.leadspace.com/
```

The script prints structured JSON with extracted details. Use `--raw` to also dump the raw text context sent to the LLM, and `--out <path>` to persist the JSON to disk.

## Next Steps

- Swap in Playwright for rich DOM capture when simple HTTP fetches are insufficient.
- Expand the LLM prompt based on desired schema and add validation/guardrails.
- Orchestrate multiple agent steps (crawl, segment, vision, etc.).
