import json
import google.generativeai as genai
from app.config import settings
from app.schemas import ParsedQuery

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def parse_user_query(query: str) -> ParsedQuery:
    prompt = f"""Analyze this query and return JSON: "{query}"
    Schema: {{"interest": "str", "audience": "str", "location": {{"city": "str|null", "state": "str|null", "country": "str|null"}}, "target_type": "individual|business", "search_queries": ["5 targeted Google search dorks for LinkedIn, Instagram, X, YouTube, Facebook, Threads, WhatsApp, Email"]}}"""
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return ParsedQuery(**json.loads(response.text))

def extract_and_filter_prospects(query: str, raw_results: list[dict]) -> list[dict]:
    if not raw_results:
        return []
    prompt = f"""Extract ONLY real, verified prospects from these search results matching "{query}". Do NOT invent names, URLs, emails, or phones.
    Allowed platforms: "LinkedIn", "Instagram", "X", "YouTube", "Facebook", "Threads", "WhatsApp", "Email", "Phone".
    Results: {json.dumps(raw_results, ensure_ascii=False)}
    Return JSON list: [{{"name": "Real Name", "location": "City, Country", "social_link": [{{"platform": "Platform", "link": "url"}}]}}]"""
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    try:
        return json.loads(response.text)
    except Exception:
        return []
