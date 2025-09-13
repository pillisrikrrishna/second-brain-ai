# backend/services/embeddings.py
"""
Embeddings Service
------------------
Converts text into embeddings (vector representation) using OpenAI API.
These embeddings are later stored in FAISS / Pinecone for semantic search.
"""

import os
import logging
from openai import OpenAI

# Create OpenAI client (requires OPENAI_API_KEY in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Choose embedding model
EMBEDDING_MODEL = "text-embedding-ada-002"  # hackathon friendly (fast + cheap)

def embed_text(text: str):
    """
    Convert input text into an embedding vector.
    
    Args:
        text (str): Input text to embed.
    
    Returns:
        list[float]: Embedding vector.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logging.exception("Embedding generation failed for text: %s", text)
        raise

def embed_batch(texts: list[str]):
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts (list[str]): Multiple input texts.
    
    Returns:
        list[list[float]]: List of embedding vectors.
    """
    if not texts:
        return []

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        logging.exception("Batch embedding generation failed")
        raise
