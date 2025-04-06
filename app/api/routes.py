# app/api/routes.py

from fastapi import APIRouter
from match_engine.match_engine import get_resume_job_similarity, classify_similarity
from llm_engine.suggestion_engine_flan import get_resume_suggestions
from api.schemas import MatchRequest, MatchResponse, SuggestRequest, SuggestResponse
from skill_engine.skill_extractor import extract_skills

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
    suggestions = get_resume_suggestions(request.resume_text, request.job_text)
    
    # NEW: Extract skills if you added that logic
    matched_skills, missing_skills = extract_skills(request.resume_text, request.job_text)

    return {
        "score": score,
        "label": label,
        "suggestions": suggestions,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }