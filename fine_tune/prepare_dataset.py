"""
prepare_dataset.py
------------------
Collects user data and produces user_training.jsonl
for potential fine-tuning of a conversational model.
"""

import json
from pathlib import Path

DATA_DIR = Path("../data")
OUTPUT_FILE = Path("user_training.jsonl")

def load_sample_data():
    """Load habits, calendar events, and notes."""
    habits = json.loads((DATA_DIR / "habits.json").read_text())
    calendar = json.loads((DATA_DIR / "calendar.json").read_text())
    notes = (DATA_DIR / "notes.txt").read_text().splitlines()
    return habits, calendar["events"], notes

def create_training_examples():
    """Transform user data into Q&A style examples for fine-tuning."""
    habits, events, notes = load_sample_data()
    examples = []

    # Habits
    for h in habits:
        q = f"When do I usually {h['habit'].lower()}?"
        a = f"You usually {h['habit'].lower()} at {h['time']} ({h['frequency']})."
        examples.append({"messages": [{"role": "user", "content": q},
                                      {"role": "assistant", "content": a}]})

    # Calendar events
    for e in events:
        q = f"When is {e['title']}?"
        a = f"{e['title']} is on {e['date']} at {e['time']} at {e['location']}."
        examples.append({"messages": [{"role": "user", "content": q},
                                      {"role": "assistant", "content": a}]})

    # Notes
    for note in notes:
        if note.strip():
            q = f"What do I need to remember about: {note[:20]}..."
            a = note
            examples.append({"messages": [{"role": "user", "content": q},
                                          {"role": "assistant", "content": a}]})
    return examples

def main():
    examples = create_training_examples()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Created {len(examples)} training examples in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
