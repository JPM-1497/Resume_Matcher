from sentence_transformers import SentenceTransformer, util

# Load the pretrained model once when this module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_resume_job_similarity(resume_text: str, job_text: str) -> float:
    """
    Compute cosine similarity between a resume and a job description
    using a SentenceTransformer embedding model.
    
    Args:
        resume_text (str): The plain text content of the resume.
        job_text (str): The plain text content of the job description.
    
    Returns:
        float: Cosine similarity score (0.0 - 1.0)
    """
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    score = util.cos_sim(resume_embedding, job_embedding).item()
    return score

def classify_similarity(score: float) -> str:
    """
    Classify a similarity score into a match label.
    
    Args:
        score (float): Cosine similarity score
    
    Returns:
        str: One of "low", "medium", or "high"
    """
    if score > 0.7:
        return "high"
    elif score > 0.5:
        return "medium"
    else:
        return "low"
