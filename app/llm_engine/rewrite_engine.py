# app/llm_engine/rewrite_engine.py

from typing import Optional
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_resume(resume_text: str, job_text: str, additional_info: Optional[str] = "") -> str:
    prompt = f"""
You are a professional resume writer. Given the original resume below and the job description, rewrite the resume to better match the job while keeping the user's experiences factual and realistic.

Include only content derived from the resume and additional notes. Do not hallucinate experiences.

### Original Resume:
{resume_text}

### Job Description:
{job_text}

### Additional Notes from User (if any):
{additional_info}

### Rewritten Resume:
"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
