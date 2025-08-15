import os
from datetime import date
import streamlit as st
from dotenv import load_dotenv

from src.parsers.resume_parser import extract_text as parse_resume
from src.parsers.jd_parser import extract_skills
from src.matching.matcher import relevance_score
from src.optimizer.ats import ats_suggestions
from src.generator.cover_letter_groq import generate_cover_letter_groq
from src.utils.text import normalize

# OCR imports for image resumes
import pytesseract
from PIL import Image

# DB imports
from database import Base, engine
from db_utils import add_application, list_applications

load_dotenv()
st.set_page_config(page_title="AI Job Application Assistant (Groq)", layout="wide")
st.title("🤖 AI Job Application Assistant")

# Create database tables if not exists
Base.metadata.create_all(bind=engine)

with st.expander("What this does"):
    st.write(
        "Upload your resume and paste a job description. "
        "Get a match score, missing keywords, ATS tips, and an AI-written cover letter via Groq. "
        "Track applications in a SQLite database."
    )

left, right = st.columns(2)

# -------------------------
# Resume Upload
# -------------------------
with left:
    st.header("1) Upload Resume")
    up = st.file_uploader(
        "Resume (PDF / DOCX / TXT / PNG / JPG)",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
    )
    resume_text = ""
    if up:
        tmp = f"tmp_{up.name}"
        with open(tmp, "wb") as f:
            f.write(up.read())
        try:
            if tmp.lower().endswith((".png", ".jpg", ".jpeg")):
                # OCR for images
                image = Image.open(tmp)
                resume_text = pytesseract.image_to_string(image)
                ext = "image"
            else:
                resume_text, ext = parse_resume(tmp)
            st.success(f"Parsed resume ({ext.upper()})")
        except Exception as e:
            st.error(f"Failed to parse resume: {e}")
            resume_text = ""
        finally:
            try:
                os.remove(tmp)
            except:
                pass
        resume_text = st.text_area("Resume Text (editable)", resume_text, height=220)

# -------------------------
# Job Description Input
# -------------------------
with right:
    st.header("2) Paste Job Description")
    default_jd = ""
    try:
        default_jd = open("data/sample_jd.txt", "r", encoding="utf-8").read()
    except Exception:
        default_jd = ""
    jd_text = st.text_area("Job Description", value=default_jd, height=260)
    company = st.text_input("Company", value="Acme Inc.")
    role = st.text_input("Role", value="Machine Learning Engineer")
    applicant_name = st.text_input("Your Name", value="Ansh")  # Changed here

st.divider()

# -------------------------
# Analyze Fit
# -------------------------
if st.button("Analyze Fit", type="primary", use_container_width=True):
    if not resume_text.strip():
        st.error("Please upload a resume with readable text.")
    elif not jd_text.strip():
        st.error("Please provide a job description.")
    else:
        resume_text_n = normalize(resume_text)
        jd_text_n = normalize(jd_text)

        c1, c2, c3 = st.columns(3)
        with c1:
            score = relevance_score(resume_text_n, jd_text_n)
            st.metric(
                "Match Score",
                f"{score['score']} / 100",
                help=f"Method: {score['method']}",
            )
        with c2:
            jd_sk = extract_skills(jd_text_n)
            st.write("**JD skills (detected)**")
            st.code(", ".join(jd_sk) or "—")
        with c3:
            ats = ats_suggestions(resume_text_n, jd_text_n)
            st.write("**Missing keywords**")
            st.code(", ".join(ats["missing_keywords"]) or "—")

        st.session_state["analysis"] = {
            "resume_text": resume_text_n,
            "jd_text": jd_text_n,
            "score": score["score"],
            "jd_skills": jd_sk,
            "missing": ats["missing_keywords"],
            "company": company,
            "role": role,
            "applicant_name": applicant_name,
        }
        st.success("Analysis ready below. Scroll for cover letter and tracker.")

# -------------------------
# Generate Cover Letter + Save to DB
# -------------------------
if "analysis" in st.session_state:
    data = st.session_state["analysis"]
    st.subheader("✍️ Generate AI Cover Letter (Groq)")
    colA, colB = st.columns([3, 1])
    with colA:
        if st.button("Generate Cover Letter", use_container_width=True):
            try:
                out = generate_cover_letter_groq(
                    resume_text=data["resume_text"],
                    jd_text=data["jd_text"],
                    applicant_name=data["applicant_name"],
                    company=data["company"],
                    role=data["role"],
                )
                st.session_state["cover_letter"] = out["cover_letter"]
                st.success("Cover letter generated.")
            except Exception as e:
                st.error(f"Failed to generate with Groq: {e}")
    with colB:
        st.write("Model:", os.getenv("GROQ_MODEL", "llama3-8b-8192"))

    st.text_area(
        "Cover Letter",
        value=st.session_state.get("cover_letter", ""),
        height=300,
    )

    st.subheader("📌 Save to Application Tracker (SQLite)")
    c1, c2, c3, c4 = st.columns([2, 1, 1, 2])
    with c1:
        link = st.text_input("Job Link (optional)", value="")
    with c2:
        status = st.selectbox(
            "Status", ["applied", "interview", "offer", "rejected"], index=0
        )
    with c3:
        follow = st.date_input("Next Follow-up", value=date.today())
    with c4:
        notes = st.text_input("Notes", value="")

    if st.button("Save Application", use_container_width=True):
        add_application(
            company=data["company"],
            role=data["role"],
            job_link=link,
            match_score=data["score"],
            status=status,
            next_followup=str(follow),
            notes=notes,
            resume_text=data["resume_text"],
            jd_text=data["jd_text"],
            cover_letter=st.session_state.get("cover_letter", ""),
        )
        st.success("Saved. See table below.")

    st.divider()
    st.subheader("📋 Applications")
    try:
        df = list_applications()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception:
        st.info("No applications yet. Save one to get started.")
