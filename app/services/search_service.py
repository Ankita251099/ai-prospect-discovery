import asyncio
import httpx
from app.config import settings
from app.utils.validators import detect_platform, extract_contacts_from_text

SERPER_URL = "https://serper.dev"

async def fetch_single_query(client: httpx.AsyncClient, q: str) -> list[dict]:
    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    try:
        resp = await client.post(SERPER_URL, json={"q": q, "num": 10}, headers=headers, timeout=15.0)
        resp.raise_for_status()
        return resp.json().get("organic", [])
    except Exception:
        return []

async def discover_raw_profiles(search_queries: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        results_nested = await asyncio.gather(*[fetch_single_query(client, q) for q in search_queries])
    seen_urls, cleaned = set(), []
    for group in results_nested:
        for item in group:
            link, title, snippet = item.get("link", ""), item.get("title", ""), item.get("snippet", "")
            if not link or link in seen_urls: continue
            seen_urls.add(link)
            platform = detect_platform(link)
            contacts = extract_contacts_from_text(f"{title} {snippet} {link}")
            if platform or contacts:
                cleaned.append({"title": title, "snippet": snippet, "url": link, "detected_platform": platform or "Website", "extracted_contacts": contacts})
    return cleaned[:25]
