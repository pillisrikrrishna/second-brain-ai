# backend/services/memory_store.py
"""
Memory Store Service
--------------------
Handles storage and retrieval of user memories (text + embeddings).
Uses FAISS for efficient vector similarity search.
"""

import faiss
import numpy as np

# Memory text storage (parallel to FAISS index)
memory_texts: list[str] = []
memory_meta: list[dict] = []

# FAISS index setup
VECTOR_DIM = 128  # same dim as mock embeddings (adjust if real model is used)
index = faiss.IndexFlatL2(VECTOR_DIM)  # L2 = Euclidean distance

def reset_store():
    """Clear all stored memories (useful for testing/demo reset)."""
    global memory_texts, memory_meta, index
    memory_texts = []
    memory_meta = []
    index = faiss.IndexFlatL2(VECTOR_DIM)

def add_memory(text: str, vector: list[float], metadata: dict = None):
    """
    Add a new memory to the store.
    Args:
        text (str): User memory text
        vector (list[float]): Embedding vector
        metadata (dict, optional): Extra info (source, timestamp, etc.)
    """
    global memory_texts, memory_meta, index
    memory_texts.append(text)
    memory_meta.append(metadata or {})
    vec = np.array([vector], dtype="float32")
    index.add(vec)

def search_memory(query_vector: list[float], k: int = 3):
    """
    Search for top-k relevant memories given a query vector.
    Args:
        query_vector (list[float]): Embedding of query text
        k (int): Number of results to return
    Returns:
        list[str]: Top matching memory texts
    """
    if len(memory_texts) == 0:
        return []

    query_vec = np.array([query_vector], dtype="float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if idx < len(memory_texts):
            results.append(memory_texts[idx])
    return results

def get_all_memories():
    """Return all stored memories (for debugging)."""
    return memory_texts
