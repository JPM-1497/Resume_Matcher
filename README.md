# 🤖 AI-Powered Resume Matcher & Optimizer

Match resumes to job descriptions using state-of-the-art NLP, and suggest personalized resume improvements using LLMs. Built with production-ready MLOps & DevOps tools.

---

## 🧠 Features

- Semantic matching between resumes and job descriptions
- LLM-generated resume suggestions tailored to job roles
- Resume search using vector similarity (FAISS or Pinecone)
- Real-time scoring and rewriting through a Streamlit UI
- Firebase-authenticated user accounts
- ML experiment tracking with MLflow
- Monitoring with Prometheus & Grafana
- Scalable infrastructure via Docker, Terraform, and AWS/GCP

---

## 🛠️ Tech Stack

| Layer            | Tool/Service                       |
|------------------|------------------------------------|
| ML/NLP           | Hugging Face Transformers, Sentence Transformers |
| LLM Suggestions  | LangChain, OpenAI API              |
| Vector Search    | FAISS / Pinecone / Weaviate        |
| Frontend         | Streamlit                          |
| Backend API      | FastAPI                            |
| Auth             | Firebase Auth / OAuth2             |
| Experimentation  | MLflow                             |
| Monitoring       | Prometheus + Grafana               |
| CI/CD            | GitHub Actions                     |
| Infrastructure   | Docker, Terraform, AWS/GCP         |

---

## 🚀 Project Structure

                           ┌────────────────────────────┐
                           │        End User (Web)      │
                           │  - Upload Resume & Job JD  │
                           └────────────┬───────────────┘
                                        │
                                        ▼
                               ┌────────────────┐
                               │  Streamlit UI  │◄──────┐
                               └────────────────┘       │
                                        │               │
     ┌──────────────────────────────────┼────────────────┼─────────────────────────┐
     │                                  ▼                ▼                         │
     │                        ┌────────────────┐   ┌─────────────────┐             │
     │                        │   FastAPI API  │   │   Firebase Auth │             │
     │                        └────────────────┘   └─────────────────┘             │
     │                                  │                ▲                         │
     │                                  ▼                │                         │
     │                  ┌────────────────────────────┐   │                         │
     │                  │ Resume/Job Similarity Model │   │     ┌────────────────┐ │
     │                  │   (HuggingFace, fine-tuned) │◄──┘     │   MLflow Model │◄┘
     │                  └────────────────────────────┘         │    Registry    │
     │                                  │                      └────────────────┘
     │                                  ▼
     │             ┌────────────────────────────────────┐
     │             │ Vector DB (FAISS/Pinecone)         │
     │             │ - Search similar jobs/resumes      │
     │             └────────────────────────────────────┘
     │                                  │
     │                                  ▼
     │            ┌─────────────────────────────────────┐
     │            │ LLM Suggestions (LangChain/OpenAI)   │
     │            │ - Rewrite & recommend improvements   │
     │            └─────────────────────────────────────┘
     │                                  │
     │                                  ▼
     │                   ┌───────────────────────────┐
     │                   │ Final Output to Streamlit │
     │                   └───────────────────────────┘
     │
     └─────────────────────────────────────────────────────────────────────────────┐
                                                                                   ▼
                                             ┌─────────────────────────────┐
                                             │ Monitoring & Observability  │
                                             │ - Prometheus + Grafana      │
                                             └─────────────────────────────┘

                                             ┌─────────────────────────────┐
                                             │   GitHub Actions (CI/CD)    │
                                             │ - Build, test, deploy       │
                                             └─────────────────────────────┘

                                             ┌─────────────────────────────┐
                                             │ Infrastructure (Terraform)  │
                                             │ - AWS/GCP, Docker, K8s      │
                                             └─────────────────────────────┘

---

## ⚙️ How It Works

1. **Upload resume and job description** via Streamlit.
2. Backend computes similarity using fine-tuned embeddings.
3. Optionally searches for similar jobs/resumes via vector DB.
4. LLM (via LangChain) analyzes the resume and job description.
5. Suggestions are returned to the user, with edit options.
6. All backend performance and model metrics are logged and visualized.

---

## 🌐 Deployment Architecture

- All services are containerized with Docker
- Infrastructure is provisioned via Terraform on AWS/GCP
- MLflow tracking server stores experiment metadata in S3/GCS
- Auth is handled via Firebase
- API is monitored using Prometheus, visualized via Grafana

---

## 🧪 Tests

- `pytest` for ML model logic
- `httpx` tests for FastAPI endpoints

---

## 🔐 Authentication

- Google Sign-In or email/password via Firebase
- User-specific history and session management

---

## 📈 Monitoring

- Metrics: model latency, match distribution, LLM cost
- Tools: Prometheus + Grafana dashboards

---

## 📦 Roadmap

- [ ] Add resume version history per user
- [ ] Enable fine-tuning UI via UI inputs
- [ ] Add PDF resume parser (e.g. `pdfminer` or `PyMuPDF`)
- [ ] Deploy on Kubernetes (EKS or GKE)

---

## 💼 Why This Project Matters

This project demonstrates end-to-end AI product development:
- Solves a real-world use case
- Applies MLOps best practices
- Integrates cutting-edge NLP & LLMs
- Built with modular, production-grade architecture

---

## 📩 Contact

For feedback or collaboration:
- [Your LinkedIn]
- [Your Email]
