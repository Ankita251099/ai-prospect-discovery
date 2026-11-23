from pydantic import BaseModel, Field
from typing import List, Optional

class ProspectRequest(BaseModel):
    query: str = Field(..., min_length=3)

class LocationInfo(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class ParsedQuery(BaseModel):
    interest: str
    audience: str
    location: LocationInfo
    target_type: str
    search_queries: List[str]

class SocialLink(BaseModel):
    platform: str
    link: str

class Prospect(BaseModel):
    name: str
    location: Optional[str] = None
    social_link: List[SocialLink]

class ProspectResponse(BaseModel):
    success: bool
    query: str
    total_prospects: int
    prospects: List[Prospect]
