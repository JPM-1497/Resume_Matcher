# app/main.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from prometheus_fastapi_instrumentator import Instrumentator
import requests 

# ---------- Logging Setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("resume_matcher_api")

# ---------- FastAPI Setup ----------
app = FastAPI(
    title="Resume Matcher & Optimizer API",
    description="API for matching resumes to job descriptions and generating suggestions.",
    version="1.0.0"
)

logger.info("🚀 FastAPI application initialized.")  # ✅ Add this here

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routes ----------
app.include_router(api_router)

# Register Prometheus metrics endpoint at /metrics
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

