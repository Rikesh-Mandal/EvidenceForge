from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.config import get_settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(get_settings().embed_model)

def encode_passages(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_embedding_model().encode(
        texts, normalize_embeddings=True, show_progress_bar=False
    )
    if vectors.shape[1] != 384:
        raise ValueError("Embedding dimension changed; migrate and reindex")
    return vectors.tolist()

