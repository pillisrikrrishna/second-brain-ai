from models.brain import SecondBrain
from services.data_ingestion import ingest_sample_data

# Initialize your Second Brain
brain = SecondBrain()

# Load sample data from data/
ingest_sample_data(brain)

print("Sample data loaded into memory store!")
