from transformers import pipeline
import json
import re
import os
import requests

# Model configuration
MODEL_NAME = os.getenv("SUGGESTION_MODEL", "google/flan-t5-base")

# Load the FLAN-T5 model pipeline once
generator = pipeline("text2text-generation", model=MODEL_NAME)

def extract_json_block(text):
    """
    Extract the first JSON block from a text string and parse it safely.
    """
    try:
        json_str = re.search(r'\{.*?\}', text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": text.strip()
        }

def get_resume_suggestions(resume_text: str, job_text: str) -> dict:
    """
    Use FLAN-T5 to extract skill matches and suggest improvements.

    Returns:
        dict: {
            'matched_skills': [...],
            'missing_skills': [...],
            'suggestions': str
        }
    """
    prompt = f"""
    You are a professional career coach helping a job applicant tailor their resume.

    TASKS:
    1. From the job description, extract 5 key skills the employer is looking for.
    2. Compare the resume to that list and identify which of those 5 skills are clearly present (matched).
    3. List which of those skills are not found or are unclear (missing).
    4. Based on the above, suggest 3 specific ways the candidate could improve their resume to better fit the job.

    The suggestions should be:
    - Short and specific
    - Human-like and helpful
    - Justified with a reason (why it matters to this job)

    FORMAT your output strictly as valid JSON:
    {{
    "matched_skills": ["..."],
    "missing_skills": ["..."],
    "suggestions": "- Suggestion 1 (reason)\n- Suggestion 2 (reason)\n- Suggestion 3 (reason)"
    }}

    Job Description:
    {job_text}

    Resume:
    {resume_text}
    """

    result = generator(prompt, max_length=1024, do_sample=False)[0]["generated_text"]
    return extract_json_block(result)
