from app.schemas import Prospect, SocialLink

def consolidate_prospects(prospects_data: list[dict]) -> list[Prospect]:
    merged = {}
    for item in prospects_data:
        name = item.get("name", "").strip()
        if len(name) < 2: continue
        key = name.lower()
        if key not in merged:
            merged[key] = {"name": name, "location": item.get("location"), "links": {}}
        for sl in item.get("social_link", []):
            p, l = sl.get("platform", "").strip(), sl.get("link", "").strip()
            if p and l and l not in merged[key]["links"]:
                merged[key]["links"][l] = SocialLink(platform=p, link=l)
    return [Prospect(name=v["name"], location=v["location"], social_link=list(v["links"].values())) for v in merged.values() if v["links"]]
