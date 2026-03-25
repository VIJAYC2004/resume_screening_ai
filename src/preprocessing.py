# src/preprocessing.py

import re
import string
from typing import List

import nltk

# Download once in setup, wrap in try/except
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_remove_stopwords(text: str) -> List[str]:
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return tokens


def preprocess(text: str) -> str:
    """
    Clean + basic token filtering.
    Sentence-transformers do not strictly need heavy preprocessing,
    but light cleaning helps. [web:1][web:5]
    """
    cleaned = clean_text(text)
    tokens = tokenize_and_remove_stopwords(cleaned)
    return " ".join(tokens)
