# app.py

import os
import tempfile

import streamlit as st

from src.config import RESUME_DIR, JD_DIR, TOP_K_DEFAULT
from src.data_loader import load_resume, load_job_description
from src.embedder import TextEmbedder
from src.ranker import rank_resumes


st.set_page_config(page_title="Resume Screening AI", layout="wide")
st.title("🔎 Resume Screening AI System")


@st.cache_resource(show_spinner=False)
def get_embedder():
    return TextEmbedder()


def save_uploaded_files(uploaded_files, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    paths = []
    for f in uploaded_files:
        path = os.path.join(target_dir, f.name)
        with open(path, "wb") as out:
            out.write(f.read())
        paths.append(path)
    return paths


tab1, tab2 = st.tabs(["Upload Files", "Use Existing Data"])

with tab1:
    st.subheader("1. Upload resumes and job description")
    uploaded_resumes = st.file_uploader(
        "Upload multiple resumes (pdf/docx/txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True
    )
    uploaded_jd = st.file_uploader(
        "Upload job description (txt/pdf/docx)", type=["txt", "pdf", "docx"]
    )

    if uploaded_resumes and uploaded_jd:
        if st.button("Run Screening (Uploads)"):
            with st.spinner("Processing uploaded files..."):
                temp_dir = tempfile.mkdtemp()
                resume_dir = os.path.join(temp_dir, "resumes")
                jd_dir = os.path.join(temp_dir, "jd")
                os.makedirs(jd_dir, exist_ok=True)

                resume_paths = save_uploaded_files(uploaded_resumes, resume_dir)

                jd_path = os.path.join(jd_dir, uploaded_jd.name)
                with open(jd_path, "wb") as out:
                    out.write(uploaded_jd.read())

                # Load texts
                resume_texts = {
                    os.path.basename(p): load_resume(p) for p in resume_paths
                }
                jd_text = load_job_description(jd_path)

                embedder = get_embedder()
                ranked = rank_resumes(
                    resume_texts=resume_texts,
                    jd_text=jd_text,
                    embedder=embedder,
                    top_k=min(TOP_K_DEFAULT, len(resume_texts)),
                )

                st.subheader("Top matching candidates")
                for i, (name, score) in enumerate(ranked, start=1):
                    st.write(f"**{i}. {name}** — similarity score: {score:.4f}")

with tab2:
    st.subheader("2. Use files from data/ directory")
    existing_resumes = [
        f for f in os.listdir(RESUME_DIR)
        if os.path.isfile(os.path.join(RESUME_DIR, f))
    ] if os.path.exists(RESUME_DIR) else []

    existing_jds = [
        f for f in os.listdir(JD_DIR)
        if f.endswith(".txt")
    ] if os.path.exists(JD_DIR) else []

    selected_resumes = st.multiselect(
        "Select resumes", existing_resumes, default=existing_resumes
    )
    selected_jd = st.selectbox("Select job description", existing_jds)

    top_k = st.slider("Top K candidates", 1, 20, TOP_K_DEFAULT)

    if st.button("Run Screening (Existing Data)"):
        if not selected_resumes or not selected_jd:
            st.warning("Please select at least one resume and a job description.")
        else:
            with st.spinner("Processing existing data..."):
                resume_texts = {}
                for fname in selected_resumes:
                    fpath = os.path.join(RESUME_DIR, fname)
                    from src.data_loader import load_resume as lr
                    resume_texts[fname] = lr(fpath)

                jd_path = os.path.join(JD_DIR, selected_jd)
                jd_text = load_job_description(jd_path)

                embedder = get_embedder()
                ranked = rank_resumes(
                    resume_texts=resume_texts,
                    jd_text=jd_text,
                    embedder=embedder,
                    top_k=min(top_k, len(resume_texts)),
                )

                st.subheader("Top matching candidates")
                for i, (name, score) in enumerate(ranked, start=1):
                    st.write(f"**{i}. {name}** — similarity score: {score:.4f}")
