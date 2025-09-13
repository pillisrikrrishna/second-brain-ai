# backend/services/data_ingestion.py
"""
Data Ingestion Service
----------------------
Collects user data (text, habits, interactions, routines, etc.),
generates embeddings, and stores them in the memory store.
"""

import datetime
from .embeddings import embed_text
from .memory_store import add_memory

def ingest_text(user_id: str, text: str, source: str = "manual"):
    """
    Ingest a single text snippet as a memory.

    Args:
        user_id (str): Unique user identifier
        text (str): Content to store
        source (str): Where the data came from (chat, calendar, notes, etc.)
    Returns:
        dict: Metadata for confirmation/logging
    """
    if not text or not text.strip():
        raise ValueError("Cannot ingest empty text")

    # 1️⃣ Create embedding
    vector = embed_text(text)

    # 2️⃣ Metadata
    metadata = {
        "user_id": user_id,
        "source": source,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # 3️⃣ Store in vector DB
    add_memory(text, vector, metadata)

    return {
        "status": "success",
        "stored_text": text,
        "metadata": metadata
    }


def bulk_ingest(user_id: str, items: list[dict]):
    """
    Ingest a list of items.
    Each item must be a dict with keys:
        { "text": "...", "source": "optional" }

    Returns:
        list of results for each item
    """
    results = []
    for item in items:
        text = item.get("text", "")
        source = item.get("source", "bulk")
        try:
            res = ingest_text(user_id, text, source)
            results.append(res)
        except Exception as e:
            results.append({"status": "error", "error": str(e), "text": text})
    return results
import json
from backend.models.brain import SecondBrain

def ingest_sample_data(brain: SecondBrain):
    with open("data/habits.json") as f:
        habits = json.load(f)
        for h in habits:
            brain.add_memory(f"Habit: {h['habit']} at {h['time']} ({h['frequency']})")

    with open("data/calendar.json") as f:
        events = json.load(f)["events"]
        for e in events:
            brain.add_memory(f"Event: {e['title']} on {e['date']} at {e['time']}")

    with open("data/notes.txt") as f:
        for line in f:
            brain.add_memory(line.strip())
    return {"status": "Demo data ingested"}