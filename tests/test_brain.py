import pytest
from backend.models.brain import SecondBrain
from backend.services.embeddings import EmbeddingService
from backend.services.predictions import PredictionService

@pytest.fixture
def brain():
    embedding_service = EmbeddingService(dimension=8)   # mock 8-dim vectors
    prediction_service = PredictionService(embedding_service)
    return SecondBrain(embedding_service, prediction_service)

def test_add_and_answer(brain):
    # Add some memories
    brain.add_memory("I love reading books at night.")
    brain.add_memory("I usually wake up at 6 AM.")
    brain.add_memory("I prefer tea over coffee.")

    # Ask a related question
    response = brain.answer_question("What time do I wake up?")
    
    assert isinstance(response, str)
    assert "wake" in response.lower() or "6" in response

def test_empty_brain_answer(brain):
    # New brain without memories
    fresh_brain = brain
    fresh_brain.memory_store = brain.memory_store.__class__(dimension=8)  # reset
    response = fresh_brain.answer_question("What is my favorite drink?")
    assert isinstance(response, str)  # should not crash
