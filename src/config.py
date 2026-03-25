# src/config.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESUME_DIR = os.path.join(BASE_DIR, "data", "resumes")
JD_DIR = os.path.join(BASE_DIR, "data", "job_descriptions")

# Pretrained sentence-transformer model
# MiniLM is light & good for semantic similarity on long texts. [web:5][web:12]
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K_DEFAULT = 5
