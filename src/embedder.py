# src/embedder.py

from typing import List
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL_NAME


class TextEmbedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]):
        """
        Returns a 2D numpy array of embeddings.
        """
        return self.model.encode(
            texts,
            batch_size=8,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,  # cosine-friendly
        )
