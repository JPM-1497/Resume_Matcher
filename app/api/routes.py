# app/api/routes.py

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from match_engine.match_engine import get_resume_job_similarity, classify_similarity
from llm_engine.suggestion_engine_flan import get_resume_suggestions
from api.schemas import MatchRequest, MatchResponse, SuggestRequest, SuggestResponse
from skill_engine.skill_extractor import extract_skills
from llm_engine.rewrite_engine import rewrite_resume
from llm_engine.skill_summary_engine import analyze_resume_skills


router = APIRouter()

@router.post("/match", response_model=MatchResponse)
def match_resume_to_job(request: MatchRequest):
    score = get_resume_job_similarity(request.resume_text, request.job_text)
    label = classify_similarity(score)
    return MatchResponse(score=score, label=label)

@router.post("/suggest", response_model=SuggestResponse)
def suggest_resume_improvements(request: SuggestRequest):
    suggestions = get_resume_suggestions(request.resume_text, request.job_text)
    return SuggestResponse(suggestions=suggestions)

@router.post("/match_and_suggest")
def match_and_suggest(request: MatchRequest):
    score = get_resume_job_similarity(request.resume_text, request.job_text)
    label = classify_similarity(score)

    # 🧠 Use GPT to analyze skills + suggestions
    skill_output = analyze_resume_skills(request.resume_text, request.job_text)

    return {
        "score": score,
        "label": label,
        "matched_skills": skill_output.get("matched_skills", []),
        "missing_skills": skill_output.get("missing_skills", []),
        "suggestions": skill_output.get("suggestions", "")
    }


class RewriteRequest(BaseModel):
    resume_text: str
    job_text: str
    additional_info: Optional[str] = ""

@router.post("/rewrite_resume")
def rewrite_resume_route(req: RewriteRequest):
    rewritten = rewrite_resume(req.resume_text, req.job_text, req.additional_info)
    return {"rewritten_resume": rewritten}