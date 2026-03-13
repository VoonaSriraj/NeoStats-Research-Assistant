"""Live web search utilities.

Uses Tavily by default (generous free tier) and fails gracefully if keys are missing.
"""

from __future__ import annotations

import logging

from config.config import TAVILY_API_KEY

logger = logging.getLogger(__name__)
_warned_missing_key: bool = False


def web_search(query: str, num_results: int = 3) -> str:
    """Run a web search and return formatted results.

    If the API key is missing or the call fails, this returns an empty string and
    logs the error instead of raising.

    Args:
        query: Search query.
        num_results: Number of results to fetch.

    Returns:
        A formatted string containing search results (title, URL, snippet),
        or an empty string on failure.
    """
    global _warned_missing_key  # noqa: PLW0603
    if not TAVILY_API_KEY:
        if not _warned_missing_key:
            logger.warning("TAVILY_API_KEY is missing; web search disabled.")
            _warned_missing_key = True
        return ""

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=TAVILY_API_KEY)
        resp = client.search(query=query, max_results=num_results)
        results = resp.get("results", []) if isinstance(resp, dict) else []

        lines: list[str] = []
        for r in results[:num_results]:
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            snippet = (r.get("content") or r.get("snippet") or "").strip()
            if not (title or url or snippet):
                continue
            lines.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}".strip())

        return "\n\n".join(lines).strip()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Web search failed: %s", exc)
        return ""


