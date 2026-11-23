from fastapi import FastAPI, HTTPException
from app.schemas import ProspectRequest, ProspectResponse
from app.services.llm_service import parse_user_query, extract_and_filter_prospects
from app.services.search_service import discover_raw_profiles
from app.services.deduplication_service import consolidate_prospects

app = FastAPI(title="AI-Powered Multi-Platform Prospect Discovery API", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "running", "docs": "/docs"}

@app.post("/prospect-discovery", response_model=ProspectResponse)
async def prospect_discovery(request: ProspectRequest):
    try:
        parsed = parse_user_query(request.query)
        raw_results = await discover_raw_profiles(parsed.search_queries)
        extracted = extract_and_filter_prospects(request.query, raw_results)
        consolidated = consolidate_prospects(extracted)
        return ProspectResponse(success=True, query=request.query, total_prospects=len(consolidated), prospects=consolidated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
