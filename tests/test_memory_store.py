import pytest
from backend.services.memory_store import MemoryStore
import numpy as np

def test_add_and_search_memory():
    store = MemoryStore(dimension=3)  # small dimension for testing

    # add a memory
    embedding = np.array([0.1, 0.2, 0.3], dtype="float32")
    text = "Went jogging in the morning"
    store.add_memory(embedding, text)

    # search with a similar vector
    query = np.array([0.1, 0.19, 0.29], dtype="float32")
    results = store.search(query, top_k=1)

    assert len(results) == 1
    assert results[0][0] == text
    assert results[0][1] >= 0  # similarity score should be non-negative
