import os
import requests

from qdrant_client import QdrantClient, models

from utils import setup_logging

logger = setup_logging()

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION_NAME")

embedding_dim = os.getenv("VECTOR_EMBEDDING_DIM")
vector_search_metric = os.getenv("VECTOR_SEARCH_METRIC", "cosine")

ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama_embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

def get_index():
    collections = client.get_collections().collections
    if collection_name not in [c.name for c in collections]:
        raise KeyError(f"Collection {collection_name} not found")
    return client

def vectorize(article: str) -> list[float]:
    response = requests.post(
        f"{ollama_host}/api/embeddings",
        json={"model": ollama_embedding_model, "prompt": article},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("embedding", [])


def upsert_vectors(index: QdrantClient, data: list[dict]):
    points = [
        models.PointStruct(id=item["id"], vector=item["vector"], payload=item.get("payload"))
        for item in data
    ]
    index.upsert(collection_name=collection_name, points=points)


def query_vectors(index: QdrantClient, vector: list[float], top_k: int, filter_query: dict | None = None):
    if len(vector) != int(embedding_dim):
        raise ValueError("Length of vector does not match the embedding dimension")
    return index.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=top_k,
        with_payload=True,
        query_filter=filter_query,
    )


if __name__ == "__main__":
    paragraph = "This is a test."
    vectorize(paragraph)
