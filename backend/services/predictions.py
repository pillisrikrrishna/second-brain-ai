# backend/services/predictions.py
"""
Predictions / Second Brain Response
-----------------------------------
Given a user query:
1️⃣ Embed the query
2️⃣ Retrieve most relevant memories
3️⃣ Generate an answer that reflects the user's own habits & knowledge
"""

import os
from .embeddings import embed_text
from .memory_store import search_memory

USE_MOCK = True  # Set to False if you have a real OpenAI API key

if not USE_MOCK and os.getenv("OPENAI_API_KEY"):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    COMPLETION_MODEL = "gpt-4o-mini"  # small/cheap model

def generate_response(user_id: str, question: str, top_k: int = 3) -> str:
    """
    Generate a 'Second Brain' style response to the user's question.

    Args:
        user_id (str): Unique user identifier (optional for now)
        question (str): The question to ask the Second Brain
        top_k (int): How many top memories to use for context

    Returns:
        str: Answer generated from relevant memories
    """
    if not question.strip():
        return "I need a question to think about!"

    # 1️⃣ Embed the query
    query_vec = embed_text(question)

    # 2️⃣ Retrieve top memories
    memories = search_memory(query_vec, k=top_k)

    context = "\n".join(memories) if memories else "No stored memories yet."

    # 3️⃣ Generate a response
    if USE_MOCK or not os.getenv("OPENAI_API_KEY"):
        # Simple mock: echo back memories + question
        if memories:
            return (
                f"🤖 (Mock Second Brain)\n"
                f"You asked: '{question}'\n"
                f"I remember these things about you:\n- "
                + "\n- ".join(memories)
                + "\nSo my guess is based on that memory."
            )
        else:
            return (
                f"🤖 (Mock Second Brain)\n"
                f"You asked: '{question}'\n"
                f"But I don't have any memories yet."
            )
    else:
        # Real OpenAI completion call
        prompt = (
            "You are the user's 'second brain'. "
            "Use the following memories to answer the question as if you are the user.\n\n"
            f"Memories:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer like the user would:"
        )
        resp = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()
