# backend/models/brain.py
"""
Second Brain Core
-----------------
High-level interface that:
  • stores user data (memories)
  • retrieves & reasons over those memories
  • produces answers in the user's own style
"""

from datetime import datetime
from services.data_ingestion import ingest_text, bulk_ingest
from services.predictions import generate_response
from services.memory_store import get_all_memories, reset_store


class SecondBrain:
    """
    Main class that represents a single user's 'second brain'.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id

    # ---- Memory Management ----
    def add_memory(self, text: str, source: str = "manual") -> dict:
        """
        Add a single memory snippet.
        """
        return ingest_text(self.user_id, text, source)

    def add_bulk_memories(self, items: list[dict]) -> list:
        """
        Add multiple memories at once.
        Each item = { "text": "...", "source": "optional" }
        """
        return bulk_ingest(self.user_id, items)

    def list_memories(self) -> list:
        """
        Retrieve all stored memories (strings only).
        (In real multi-user app you’d filter by user_id,
         but demo version shares a single FAISS index.)
        """
        return get_all_memories()

    def clear_memories(self):
        """
        Wipe all memories for demo or testing.
        NOTE: Clears global FAISS index (all users).
        """
        reset_store()

    # ---- Brain Response ----
    def ask(self, question: str, top_k: int = 3) -> str:
        """
        Ask the Second Brain a question.
        Returns an answer based on stored memories.
        """
        return generate_response(self.user_id, question, top_k=top_k)


# Optional helper for quick demo usage
def demo_brain():
    """
    Quick interactive demo if this file is run directly.
    """
    brain = SecondBrain(user_id="demo")
    print("=== Second Brain Demo ===")
    brain.add_memory("I enjoy evening walks near the lake.")
    brain.add_memory("My favorite movie is Interstellar.")
    print(brain.ask("What movie do I like?"))
    print(brain.ask("Do I like to walk?"))
    print("All memories:", brain.list_memories())


if __name__ == "__main__":
    demo_brain()
