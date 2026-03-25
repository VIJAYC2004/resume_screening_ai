# src/ranker.py

from typing import Dict, List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity_scores(
    jd_embedding: np.ndarray, resume_embeddings: np.ndarray
) -> np.ndarray:
    """
    jd_embedding: shape (1, d)
    resume_embeddings: shape (n, d)
    returns: shape (n,)
    """
    sims = cosine_similarity(jd_embedding, resume_embeddings)  # (1, n)
    return sims.flatten()


def rank_resumes(
    resume_texts: Dict[str, str],
    jd_text: str,
    embedder,
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """
    Returns list of (resume_filename, score) sorted desc.
    """
    resume_names = list(resume_texts.keys())
    texts = list(resume_texts.values())

    from .preprocessing import preprocess

    jd_clean = preprocess(jd_text)
    resumes_clean = [preprocess(t) for t in texts]

    jd_embedding = embedder.encode([jd_clean])
    resume_embeddings = embedder.encode(resumes_clean)

    scores = compute_similarity_scores(jd_embedding, resume_embeddings)

    ranked_indices = np.argsort(scores)[::-1]
    ranked = [(resume_names[i], float(scores[i])) for i in ranked_indices]

    return ranked[:top_k]
