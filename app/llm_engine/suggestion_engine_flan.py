from transformers import pipeline
import json
import re
import os
import requests
from openai import OpenAI

# Model configuration
MODEL_NAME = os.getenv("SUGGESTION_MODEL", "google/flan-t5-base")

# Load the FLAN-T5 model pipeline once
generator = pipeline("text2text-generation", model=MODEL_NAME)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def summarize_skills(resume: str, job: str, matched: list, missing: list) -> str:
    """
    Use GPT-4 to generate a natural language summary of matched and missing skills.
    """
    prompt = f"""
You are a professional resume reviewer.

1. Summarize how the resume aligns with the job using the matched skills.
2. Briefly describe gaps or missing qualifications using the missing skills.
3. Keep the tone positive, concise, and helpful (2 paragraphs max).

Resume:
{resume}

Job Description:
{job}

Matched Skills:
{", ".join(matched)}

Missing Skills:
{", ".join(missing)}
"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()

def get_resume_suggestions(resume_text: str, job_text: str, matched_skills: list = [], missing_skills: list = []) -> dict:

    """
    Use FLAN-T5 to extract skill matches and suggest improvements.

    Returns:
        dict: {
            'matched_skills': [...],
            'missing_skills': [...],
            'suggestions': str,
            'skill_summary': str
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

Respond ONLY in this exact JSON format — no explanations, no markdown, no commentary:

{{
  "matched_skills": ["Skill A", "Skill B", "Skill C"],
  "missing_skills": ["Skill X", "Skill Y"],
  "suggestions": "- Improve XYZ (because...)\n- Add ABC (because...)\n- Clarify LMN (because...)"
}}
Job Description:
{job_text}

Resume:
{resume_text}
"""

    result = generator(prompt, max_length=1024, do_sample=False)[0]["generated_text"]
    parsed = extract_json_block(result)

    # Add the LLM-generated summary
    skill_summary = summarize_skills(resume_text, job_text, parsed.get("matched_skills", []), parsed.get("missing_skills", []))
    parsed["skill_summary"] = skill_summary

    return parsed
