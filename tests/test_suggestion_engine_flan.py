from app.llm_engine.suggestion_engine_flan import get_resume_suggestions

resume = "Marketing analyst with 3 years of experience, skilled in Excel and basic SQL."
job = "Looking for a data analyst with strong SQL, Python, and Power BI skills."

suggestions = get_resume_suggestions(resume, job)
print("\nResume Suggestions:\n")
print(suggestions)
