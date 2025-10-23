"""Agentic analyzer using function calling for product extraction."""
from __future__ import annotations

import json
from openai import AzureOpenAI

from ..schemas.product import ProductSnapshot
from .tools.fetcher import fetch_page_text, get_fetch_page_text_tool
from .utils.tool_handler import ToolHandler, ToolRegistry


AGENTIC_SYSTEM_PROMPT = (
    "You are an agentic product intelligence assistant. Your task is to extract structured "
    "product data and generate insights from web pages to populate a ProductSnapshot schema.\n\n"
    "You have access to a fetch_page_text tool that allows you to retrieve and extract text "
    "from any URL. Use this tool strategically to gather information needed to complete the "
    "product snapshot.\n\n"
    "Guidelines:\n"
    "- Always populate the ProductSnapshot schema exactly using evidence from retrieved content\n"
    "- Write in a neutral, professional tone\n"
    "- Keep numeric values as numbers\n"
    "- Ensure every URL is an https link\n"
    "- If information is unavailable, return nulls or empty lists as appropriate\n"
    "- Do not fabricate information - only use verified details from the pages you fetch\n"
    "- Be strategic about which URLs to fetch; prioritize pages that will give you the most relevant information\n"
    "- You may call the fetch_page_text tool multiple times if needed to gather comprehensive information"
)


def extract_product_snapshot_agentic(
    client: AzureOpenAI,
    deployment: str,
    initial_url: str,
) -> ProductSnapshot:
    """Extract product data using agentic function calling."""
    
    # Setup tool registry and handler
    registry = ToolRegistry()
    registry.register(
        "fetch_page_text",
        get_fetch_page_text_tool(),
        fetch_page_text
    )
    tool_handler = ToolHandler(registry)
    
    tools = registry.get_all_schemas()
    
    messages = [
        {
            "role": "user",
            "content": (
                f"Extract product information and create a ProductSnapshot from this URL: {initial_url}\n\n"
                "Use the fetch_page_text tool to retrieve content from the URL and any related pages you need. "
                "Then provide your analysis in the ProductSnapshot format as a valid JSON object.\n\n"
                "Only return valid JSON for the ProductSnapshot, no other text. "
                "Make sure to use the fetch_page_text tool to get the actual page content before analyzing."
            )
        }
    ]
    
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        response = client.beta.chat.completions.parse(
            model=deployment,
            messages=messages,
            tools=tools,
            response_format=ProductSnapshot,
        )
        
        if response.choices[0].message.tool_calls:
            tool_calls = response.choices[0].message.tool_calls
            
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls
                ]
            })
            
            tool_results = tool_handler.execute_parallel(tool_calls)
            messages.append(tool_handler.build_tool_response_message(tool_results))
        else:
            parsed = response.choices[0].message.parsed
            if parsed:
                return parsed
            break
    
    raise RuntimeError(
        f"Failed to extract product snapshot after {max_iterations} iterations"
    )
