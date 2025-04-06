import re
from typing import List, Tuple

# A sample list of common skills. You can expand this or load from a file.
COMMON_SKILLS = [
    "python", "django", "flask", "pandas", "numpy", "jupyter notebooks", "pyspark", "fastapi",
    "sql", "postgresql", "mysql", "sql server", "oracle", "nosql", "mongodb", "t-sql", "pl/sql", "query optimization",
    "excel", "power query", "vba", "pivot tables", "power pivot", "excel macros", "data modeling", "conditional formatting",
    "tableau", "power bi", "data storytelling", "interactive dashboards", "tableau prep", "data blending", "data aggregation",
    "power bi", "dax", "power query", "power pivot", "power bi service", "report design", "interactive visualizations", "power bi desktop",
    "aws", "ec2", "s3", "lambda", "rds", "cloudformation", "aws glue", "athena", "elastic beanstalk", "redshift", "sagemaker", "cloudwatch",
    "docker", "containerization", "docker compose", "docker swarm", "kubernetes", "ci/cd", "virtualization", "microservices",
    "kubernetes", "container orchestration", "helm", "pods", "kubernetes clusters", "docker", "kubernetes services", "kubernetes deployment", "container management",
    "machine learning", "supervised learning", "unsupervised learning", "model training", "model evaluation", "feature engineering", "cross-validation", "model tuning",
    "data analysis", "descriptive analytics", "predictive analytics", "exploratory data analysis", "eda", "data cleaning", "data transformation", "data aggregation", "statistical analysis",
    "communication", "data storytelling", "presentation skills", "technical writing", "stakeholder communication", "cross-functional collaboration", "technical documentation",
    "teamwork", "agile methodology", "scrum", "collaborative development", "peer reviews", "team leadership", "conflict resolution", "project management",
    "fastapi", "restful apis", "web development", "python frameworks", "asynchronous programming", "api endpoints", "http methods", "web services",
    "pandas", "dataframes", "data cleaning", "data manipulation", "merging data", "groupby", "time series analysis", "data aggregation",
    "numpy", "arrays", "matrix operations", "linear algebra", "numerical computations", "vectorization", "mathematical modeling", "multi-dimensional arrays",
    "tensorflow", "neural networks", "deep learning", "tensorflow lite", "tensorflow hub", "keras", "model deployment", "image recognition",
    "pytorch", "neural networks", "deep learning", "autograd", "tensor computation", "model training", "gpu acceleration", "transfer learning",
    "data visualization", "matplotlib", "seaborn", "plotly", "ggplot2", "d3.js", "charting", "dashboard design", "interactive visualizations", "storytelling with data",
    "statistics", "hypothesis testing", "a/b testing", "regression analysis", "probability theory", "sampling", "descriptive statistics", "statistical models",
    "azure", "azure machine learning", "azure databricks", "azure functions", "azure sql database", "azure synapse analytics", "azure blob storage",
    "gcp", "google bigquery", "google kubernetes engine", "google cloud storage", "google compute engine", "google data studio", "google ai",
    "problem solving", "critical thinking", "root cause analysis", "optimization", "algorithmic thinking", "decision making", "troubleshooting", "logical thinking",
    "data engineering", "data pipelines", "etl", "apache kafka", "spark", "hadoop", "data warehousing", "data lake", "batch processing",
    "nlp", "text mining", "sentiment analysis", "named entity recognition", "tokenization", "word embeddings", "text classification", "chatbots", "speech recognition",
    "deep learning", "neural networks", "cnn", "rnn", "gan", "backpropagation", "autoencoders", "model optimization", "transfer learning",
]

def clean_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

def extract_skills(resume_text: str, job_text: str) -> Tuple[List[str], List[str]]:
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    matched = []
    missing = []

    for skill in COMMON_SKILLS:
        if skill in job_text:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing
