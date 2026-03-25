# src/main.py

import argparse
import os

from .config import RESUME_DIR, JD_DIR, TOP_K_DEFAULT
from .data_loader import load_all_resumes, load_job_description, list_job_descriptions
from .embedder import TextEmbedder
from .ranker import rank_resumes


def parse_args():
    parser = argparse.ArgumentParser(description="Resume Screening AI System")
    parser.add_argument(
        "--jd",
        type=str,
        required=False,
        help="Path to job description .txt file (default: first in job_descriptions/)",
    )
    parser.add_argument(
        "--resumes_dir",
        type=str,
        default=RESUME_DIR,
        help="Directory containing resumes",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=TOP_K_DEFAULT,
        help="Number of top candidates to show",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    resumes = load_all_resumes(args.resumes_dir)
    if not resumes:
        print(f"No resumes found in {args.resumes_dir}")
        return

    jd_path = args.jd
    if not jd_path:
        jd_files = list_job_descriptions(JD_DIR)
        if not jd_files:
            print(f"No job descriptions found in {JD_DIR}")
            return
        jd_path = jd_files[0]

    jd_text = load_job_description(jd_path)

    print(f"Loaded {len(resumes)} resumes from {args.resumes_dir}")
    print(f"Using job description: {jd_path}")

    embedder = TextEmbedder()

    ranked = rank_resumes(
        resume_texts=resumes,
        jd_text=jd_text,
        embedder=embedder,
        top_k=args.top_k,
    )

    print("\nTop matching candidates:")
    for i, (name, score) in enumerate(ranked, start=1):
        print(f"{i}. {name} - score: {score:.4f}")


if __name__ == "__main__":
    main()
