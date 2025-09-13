# backend/services/embeddings.py
"""
Embeddings Service (Mock Version)
---------------------------------
Since no OpenAI API key is available, this module generates mock embeddings
so the rest of the system (memory store + retrieval) still works.
When you get an API key, switch USE_MOCK = False to use real embeddings.
"""

import hashlib
import numpy as np
import os

USE_MOCK = True  # set to False when real API key is available

# Try importing OpenAI only if key is set
if not USE_MOCK and os.getenv("OPENAI_API_KEY"):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    EMBEDDING_MODEL = "text-embedding-ada-002"

def _mock_embed(text: str, dim: int = 128):
    """
    Generate a deterministic fake embedding vector from text.
    Uses SHA256 hash to create pseudo-random numbers.
    """
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    nums = [int(h[i:i+4], 16) % 1000 for i in range(0, len(h), 4)]
    # normalize to 0-1 range
    arr = np.array(nums[:dim]) / 1000.0
    return arr.tolist()

def embed_text(text: str):
    """
    Generate an embedding vector for a single text.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    if USE_MOCK or not os.getenv("OPENAI_API_KEY"):
        return _mock_embed(text)
    else:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding

def embed_batch(texts: list[str]):
    """
    Generate embeddings for a list of texts.
    """
    if not texts:
        return []

    return [embed_text(t) for t in texts]
