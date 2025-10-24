import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume_skills(resume_text: str, job_text: str) -> dict:
    """
    Uses GPT to compare a resume to a job description and return matched/missing skills and suggestions.
    """
    prompt = f"""
You are a professional resume reviewer.

Given the resume and job description below:
1. Identify 5 key skills from the job description.
2. Determine which of these skills are present in the resume (matched).
3. Determine which are missing.
4. Suggest 3 ways to improve the resume for this job (short, specific, and justified).

Respond ONLY in this exact JSON format with NO extra commentary:

{{
  "matched_skills": ["Skill A", "Skill B"],
  "missing_skills": ["Skill C"],
  "suggestions": "- Improve XYZ (because...)\n- Add ABC (because...)\n- Clarify LMN (because...)"
}}

Resume:
{resume_text}

Job Description:
{job_text}
"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    raw_response = response.choices[0].message.content.strip()

    # Debug print to help trace format issues
    print("🧪 GPT RESPONSE:", raw_response)

    # Try loading response as JSON, fallback if invalid
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": "❌ Failed to parse GPT response.",
            "skill_summary": raw_response or "⚠️ No response from model."
        }
