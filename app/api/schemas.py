# app/api/schemas.py

from pydantic import BaseModel

# Input model for /match and /match_and_suggest
class MatchRequest(BaseModel):
    resume_text: str
    job_text: str

# Output model for /match
class MatchResponse(BaseModel):
    score: float
    label: str

# Input model for /suggest
class SuggestRequest(BaseModel):
    resume_text: str
    job_text: str

# Output model for /suggest
class SuggestResponse(BaseModel):
    suggestions: str
