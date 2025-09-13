# Second Brain AI

**Second Brain AI** is a personal AI assistant that learns from your habits, routines, calendar events, and notes to act as a “second brain.” You can ask it questions, track your past interactions, and get insights about your behavior.

---

## Features

- **Chat with your Second Brain** – Ask questions about your habits, calendar, or personal notes.
- **Memory & History** – All interactions are logged and visible in the History Panel.
- **Insights Dashboard** – Shows analytics about habits and routines.
- **Data Integration** – Load sample habits, calendar events, and notes for quick demos.
- **Future Fine-Tuning** – Prepare personalized datasets (`user_training.jsonl`) for AI fine-tuning.

---

## Project Structure

second-brain-ai/
├── backend/ # Core AI + APIs
│ ├── app.py # FastAPI/Flask entry point
│ ├── models/
│ │ ├── brain.py # Second Brain logic (RAG + fine-tune)
│ │ ├── user_profile.py # Schema for habits, routines, interactions
│ ├── services/
│ │ ├── data_ingestion.py # Collect data (notes, calendar, chats)
│ │ ├── embeddings.py # Convert user data → vectors
│ │ ├── memory_store.py # Vector DB (FAISS / Pinecone)
│ │ ├── predictions.py # Habit/routine prediction (optional)
│ ├── requirements.txt
│
├── frontend/ # Chat interface
│ ├── src/
│ │ ├── App.js
│ │ ├── App.css
│ │ └── components/
│ │ ├── ChatBox.js
│ │ ├── HistoryPanel.js
│ │ └── Insights.js
│ └── package.json
│
├── data/ # Sample user data
│ ├── habits.json
│ ├── calendar.json
│ └── notes.txt
│
├── fine_tune/ # Fine-tuning dataset prep
│ ├── prepare_dataset.py
│ └── user_training.jsonl
│
├── docs/ # Hackathon documentation
│ ├── flowchart.png
│ ├── pitch.md
│ └── demo_script.md
│
├── tests/ # Unit tests
│ ├── test_memory_store.py
│ └── test_brain.py
│
└── README.md # Project overview

---


---

## Setup Instructions

### 1. Backend
1. Navigate to the backend folder:
   ```bash
   cd backend
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the backend server:

bash
Copy code
uvicorn app:app --reload --port 8000
Optional: Load sample data for demo:

bash
Copy code
python load_sample_data.py
2. Frontend
Navigate to the frontend folder:

bash
Copy code
cd frontend
Install dependencies:

bash
Copy code
npm install
Start the frontend server:

bash
Copy code
npm start
Open http://localhost:3000 in your browser.

3. Running Tests
From the project root:

bash
Copy code
pytest -v
Usage
Ask a question in the ChatBox.

View your conversation history in HistoryPanel.

Check personal analytics in the Insights panel.

Refresh Insights to see updated analytics after adding data.

Tech Stack
Backend: Python, FastAPI / Flask, FAISS, OpenAI Embeddings

Frontend: React.js

Data: JSON, Notes, Calendar

Testing: pytest

Future Enhancements
User authentication and multiple user support.

Persistent storage in PostgreSQL/MongoDB.

More advanced AI fine-tuning for highly personalized responses.

Mobile-friendly UI and notifications.

Hackathon Demo
Follow docs/demo_script.md for step-by-step demo instructions.

Reference docs/pitch.md for problem statement and solution explanation.


This README.md:
- Explains the **project purpose** clearly.
- Includes **setup & running instructions** for backend and frontend.
- Provides a **folder overview**.

