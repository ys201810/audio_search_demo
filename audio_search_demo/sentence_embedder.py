# coding=utf-8
from sentence_transformers import SentenceTransformer

class SentenceEmbedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def get_embedding_vector(self, sentences: list):
        embeddings = self.model.encode(sentences, show_progress_bar=True)
        return embeddings


