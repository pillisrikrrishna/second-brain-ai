# Second Brain AI – Hackathon Pitch

## 1. Problem Statement
People today struggle to remember and organize their daily habits, routines, notes, and interactions. Important information is scattered across apps, calendars, and personal notes, making it hard to recall and act upon efficiently.

## 2. Solution
**Second Brain AI** is a personal AI assistant that acts as your “second brain.” It:
- Learns from your **habits, routines, notes, and calendar events**
- Stores information in a **memory store** (vector database)
- Answers questions as if it knows you personally
- Provides insights into your behavior and routines

Users can interact with it via a **friendly chat interface**.

## 3. Tech Stack
- **Backend**: Python, FastAPI (or Flask), LangChain-style RAG memory
- **Frontend**: React.js (ChatBox, HistoryPanel, Insights)
- **Data Storage**: FAISS (in-memory vector DB) for embeddings
- **AI/Embeddings**: OpenAI embeddings (or mocked for demo)
- **Testing**: pytest

## 4. Key Features
- **Chat with your Second Brain**: Ask questions about your routines, habits, or past notes.
- **Memory & History**: Keeps track of all interactions in a structured history panel.
- **Insights Dashboard**: Provides analytics and trends about your behavior.
- **Sample Data Integration**: Quickly ingest habits, calendar events, and notes for demo purposes.
- **Future-Ready**: Supports fine-tuning with your own data (`user_training.jsonl`) for personalized responses.

## 5. Demo Highlights
- Ask “When is my Team Meeting?” → AI responds correctly.
- Ask “What is my favorite habit?” → AI recalls the stored habits.
- Refresh Insights → See behavior analytics in real-time.

## 6. Why it Matters
- Helps users remember important tasks and personal preferences.
- Acts as a **personal assistant that truly understands you**.
- Demonstrates the power of **AI-driven personal knowledge management**.

---
