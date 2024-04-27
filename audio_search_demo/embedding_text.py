# coding=utf-8
from sentence_transformers import SentenceTransformer


def run(model_name: str, sentences: list):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences, show_progress_bar=True)
    return embeddings

