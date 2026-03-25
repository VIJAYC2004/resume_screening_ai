# src/data_loader.py

import os
from typing import Dict, Tuple, List

from PyPDF2 import PdfReader
import docx


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


def read_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_resume(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext in [".docx"]:
        return read_docx(path)
    elif ext in [".txt"]:
        return read_txt(path)
    else:
        raise ValueError(f"Unsupported resume format: {ext}")


def load_all_resumes(resume_dir: str) -> Dict[str, str]:
    resumes = {}
    for fname in os.listdir(resume_dir):
        fpath = os.path.join(resume_dir, fname)
        if os.path.isfile(fpath):
            try:
                resumes[fname] = load_resume(fpath)
            except Exception as e:
                print(f"Failed to read {fname}: {e}")
    return resumes


def load_job_description(path: str) -> str:
    # assume txt for simplicity
    return read_txt(path)


def list_job_descriptions(jd_dir: str) -> List[str]:
    return [
        os.path.join(jd_dir, f)
        for f in os.listdir(jd_dir)
        if f.endswith(".txt")
    ]
