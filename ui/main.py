import streamlit as st
import requests
import docx2txt
import PyPDF2
import os

API_URL = os.getenv("API_URL", "http://api:8000")
JSEARCH_URL = os.getenv("JSEARCH_URL", "https://jsearch.p.rapidapi.com/search")
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "")

st.set_page_config(page_title="Resume Matcher & Optimizer", layout="wide")

# --- Styles ---
st.markdown("""
    <style>
    .main h1 {
        margin-top: -50px;  /* Raise title */
        margin-bottom: 0px;  /* Reduce spacing below */
        text-align: center;
        color: #2E86AB;
        font-size: 2rem;
    }
    .job-cards {
        max-height: 620px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .col-box {
        #border: 1px solid #e0e0e0;
        #border-radius: 8px;
        padding: 15px;
        background-color: #fafafa;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📄 Resume Matcher & Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your resume and compare it against live job listings</p>", unsafe_allow_html=True)
st.divider()

# --- State Initialization ---
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""
if "selected_job_index" not in st.session_state:
    st.session_state["selected_job_index"] = 0
if "job_results" not in st.session_state:
    st.session_state["job_results"] = []

# --- Centered Upload & Search ---
if not st.session_state.show_results:
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("### 📎 Upload your Resume (PDF, DOCX, or TXT)")
        uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt"])

        if uploaded_file:
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type == "pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                st.session_state.resume_text = "\n".join([page.extract_text() or "" for page in reader.pages])
            elif file_type == "docx":
                st.session_state.resume_text = docx2txt.process(uploaded_file)
            elif file_type == "txt":
                st.session_state.resume_text = uploaded_file.read().decode("utf-8")

        st.markdown("### 🔍 Search for Jobs")
        job_title = st.text_input("Job Title", value="Data Analyst")
        city = st.text_input("City", value="Austin")
        state = st.text_input("State", value="TX")
        num_results = st.slider("Number of Job Results", min_value=1, max_value=10, value=5)
        remote_only = st.checkbox("Remote Only", value=True)

        if st.button("Search Jobs & Match"):
            if not st.session_state.resume_text:
                st.warning("Please upload a resume to continue.")
            else:
                st.session_state.update({
                    "job_title": job_title,
                    "city": city,
                    "state": state,
                    "remote_only": remote_only,
                    "num_results": num_results,
                    "show_results": True,
                    "selected_job_index": 0
                })
                st.experimental_rerun()

# --- Results View with 3 Columns ---
else:
    col1, col2, col3 = st.columns([1, 2, 1])

    # --- Column 1: Resume & Input Fields ---
    with col1:
        #st.markdown('<div class="col-box">', unsafe_allow_html=True)
        st.markdown("### 📎 Upload your Resume")
        uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt"])
        if uploaded_file:
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type == "pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                st.session_state.resume_text = "\n".join([page.extract_text() or "" for page in reader.pages])
            elif file_type == "docx":
                st.session_state.resume_text = docx2txt.process(uploaded_file)
            elif file_type == "txt":
                st.session_state.resume_text = uploaded_file.read().decode("utf-8")

        st.markdown("### 🔍 Search for Jobs")
        job_title = st.text_input("Job Title", value=st.session_state["job_title"])
        city = st.text_input("City", value=st.session_state["city"])
        state = st.text_input("State", value=st.session_state["state"])
        num_results = st.slider("Number of Job Results", min_value=1, max_value=10, value=st.session_state["num_results"])
        remote_only = st.checkbox("Remote Only", value=st.session_state["remote_only"])

        if st.button("🔁 Search Again"):
            st.session_state.update({
                "job_title": job_title,
                "city": city,
                "state": state,
                "remote_only": remote_only,
                "num_results": num_results,
                "selected_job_index": 0
            })
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Column 2: Job Selection ---
    with col2:
        #st.markdown('<div class="col-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Matched Jobs")

        headers = {
            "X-RapidAPI-Key": JSEARCH_API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        query_parts = [st.session_state["job_title"]]
        if st.session_state["city"] and st.session_state["state"]:
            query_parts.append(f'in {st.session_state["city"]}, {st.session_state["state"]}')
        if st.session_state["remote_only"]:
            query_parts.append("or Remote")
        formatted_query = " ".join(query_parts)

        params = {
            "query": formatted_query,
            "page": "1",
            "num_pages": "1"
        }

        response = requests.get(JSEARCH_URL, headers=headers, params=params)

        if response.status_code == 200:
            jobs = response.json().get("data", [])[:st.session_state["num_results"]]
            st.session_state.job_results = []

            for i, job in enumerate(jobs):
                job_payload = {
                    "resume_text": st.session_state.resume_text,
                    "job_text": job.get("job_description", "")
                }

                match_response = requests.post(f"{API_URL}/match_and_suggest", json=job_payload)
                if match_response.status_code == 200:
                    result = match_response.json()
                    st.session_state.job_results.append({
                        "job": job,
                        "result": result
                    })

            # Sort jobs by descending score
            sorted_jobs = sorted(
                enumerate(st.session_state.job_results),
                key=lambda x: x[1]["result"]["score"],
                reverse=True
            )

            for i, data in sorted_jobs:
                job = data["job"]
                result = data["result"]
                score_pct = int(result["score"] * 100)
                job_str = f"{job.get('job_title')} - {job.get('job_city')}, {job.get('job_state')} - {score_pct}% Match"
                
                if st.button(job_str, key=f"job_btn_{i}"):
                    st.session_state["selected_job_index"] = i                
                
                if job.get("job_description"):
                    with st.expander("📋 View Full Job Description"):
                        st.markdown(job.get("job_description"))

        else:
            st.error("❌ Failed to fetch job listings.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Column 3: Skills / Suggestions ---
    with col3:
        selected = st.session_state.get("selected_job_index", 0)
        if len(st.session_state.job_results) > selected:
            result = st.session_state.job_results[selected]["result"]

            st.markdown("### 🧠 Skill Breakdown & Suggestions")

            matched = result.get("matched_skills", [])
            missing = result.get("missing_skills", [])
            suggestions = result.get("suggestions", "")

            if matched:
                st.markdown("**✅ Matched Skills:**")
                st.markdown(", ".join(matched))
            else:
                st.markdown("**✅ Matched Skills:** None detected")

            if missing:
                st.markdown("**⚠️ Missing Skills:**")
                st.markdown(", ".join(missing))
            else:
                st.markdown("**⚠️ Missing Skills:** None detected")

            st.markdown("**📝 Suggestions:**")
            # Try to format the suggestions cleanly if it's a bulleted string
            for line in suggestions.split("\n"):
                if line.strip():
                    st.markdown(f"- {line.strip()}")

        else:
            st.markdown("Select a job to see skill analysis.")