import re
from typing import Optional

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\+?\d[\d\s\-().]{8,16}\d"
WA_REGEX = r"(https?://(?:wa\.me|api\.whatsapp\.com)/[^\s\"'<>]+)"

def extract_contacts_from_text(text: str) -> list[dict]:
    contacts = []
    if not text:
        return contacts
    for email in set(re.findall(EMAIL_REGEX, text)):
        if not email.endswith((".png", ".jpg", ".jpeg", ".gif")):
            contacts.append({"platform": "Email", "link": f"mailto:{email.lower()}"})
    for wa in set(re.findall(WA_REGEX, text)):
        contacts.append({"platform": "WhatsApp", "link": wa})
    for phone in set(re.findall(PHONE_REGEX, text)):
        cleaned = re.sub(r"[^\d+]", "", phone)
        if 10 <= len(cleaned) <= 15:
            contacts.append({"platform": "Phone", "link": f"tel:{cleaned}"})
    return contacts

def detect_platform(url: str) -> Optional[str]:
    u = url.lower()
    if "://linkedin.com" in u or "://linkedin.com" in u: return "LinkedIn"
    if "://instagram.com" in u and "/p/" not in u and "/reel/" not in u: return "Instagram"
    if ("://x.com" in u or "://twitter.com" in u) and "/status/" not in u: return "X"
    if "://youtube.com@" in u or "://youtube.comchannel/" in u or "://youtube.comc/" in u: return "YouTube"
    if "://facebook.com" in u and "/posts/" not in u and "/videos/" not in u: return "Facebook"
    if "threads.net/@" in u: return "Threads"
    if "wa.me/" in u or "://whatsapp.com" in u: return "WhatsApp"
    return None
