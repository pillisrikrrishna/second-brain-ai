# backend/app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import os

# Import your project modules (implement these under backend/services and backend/models)
# If you haven't implemented them yet, create simple stubs with the same function names.
try:
    from services.embeddings import embed_text
    from services.memory_store import add_memory as memory_add, search_memory
    from models.brain import generate_response
    from services.data_ingestion import ingest_demo_data
except Exception as e:
    # If imports fail, log a friendly message. For hackathon, create stubs if needed.
    logging.warning("Some imports failed in app.py. Make sure services/ and models/ are implemented. Error: %s", e)

    # --- Minimal fallback stubs so app still runs during early dev/demo ---
    def embed_text(text: str):
        # returns a mock vector (list of floats)
        return [float(abs(hash(text)) % 1000) / 1000.0]

    _MEMORY = []
    def memory_add(text, vector=None):
        _MEMORY.append({"text": text, "vector": vector})
    def search_memory(query, k=3):
        # naive text-match fallback
        results = [m["text"] for m in _MEMORY if query.lower() in m["text"].lower()]
        return results[:k]

    def generate_response(question: str, context: Optional[List[str]] = None):
        ctx = "\n".join(context or [])
        return f"(mock) Based on context: {ctx}\nAnswer to '{question}' as the user."

    def ingest_demo_data():
        memory_add("I like Italian food and pasta.")
        memory_add("I usually workout at 7am before work.")
        memory_add("Project deadline is on 2025-10-01.")
        return {"status": "demo data ingested"}

# --- FastAPI app setup ---
app = FastAPI(title="Second Brain AI - Backend")

# Allow requests from local frontend during hackathon
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response Models ---
class AddMemoryRequest(BaseModel):
    text: str
    source: Optional[str] = "manual"
    metadata: Optional[dict] = None

class AskRequest(BaseModel):
    question: str
    k: Optional[int] = 3  # number of retrieved memories to include

class IngestResult(BaseModel):
    status: str

# --- Endpoints ---
@app.post("/add_memory/", status_code=201)
async def add_memory_api(req: AddMemoryRequest):
    """
    Add a text memory into the vector DB.
    - embed_text: converts text -> vector
    - memory_add: stores text + vector in your memory store
    """
    try:
        vector = embed_text(req.text)
        memory_add(req.text, vector)
        return {"status": "Memory added", "text": req.text}
    except Exception as e:
        logging.exception("Failed to add memory")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_brain/")
async def ask_brain(req: AskRequest):
    """
    Query the Second Brain:
    1. Use search_memory to get top-k relevant memories (RAG).
    2. Pass question + retrieved context to generate_response (LLM).
    """
    try:
        # 1) Retrieve relevant memories
        memories = search_memory(req.question, k=req.k)

        # 2) Generate answer using your brain model (wrap LLM calls here)
        answer = generate_response(req.question, memories)

        return {
            "question": req.question,
            "context": memories,
            "answer": answer
        }
    except Exception as e:
        logging.exception("ask_brain failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest_demo/", response_model=IngestResult)
async def ingest_demo():
    """
    Ingest some demo/sample user data (useful for hackathon demo).
    Implement ingest_demo_data() in services/data_ingestion.py to load from data/
    """
    try:
        result = ingest_demo_data()
        return result
    except Exception as e:
        logging.exception("ingest_demo failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/trigger_fine_tune/")
async def trigger_fine_tune():
    """
    OPTIONAL: endpoint that triggers fine-tuning or adaptation flow.
    Implementation depends on which provider you use. For hackathon, this can be mocked.
    """
    try:
        # Placeholder: return success for demo
        # Replace with code that prepares jsonl, uploads to fine-tune API, monitors job.
        return {"status": "fine-tune job started (mock)", "job_id": None}
    except Exception as e:
        logging.exception("trigger_fine_tune failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Run instructions for local dev ---
# Use: uvicorn backend.app:app --reload --port 8000
# (from project root)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
