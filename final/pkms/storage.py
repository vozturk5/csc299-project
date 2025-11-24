import os
import json

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notes.json")

def load_notes():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_PATH, "w") as f:
        json.dump(notes, f, indent=2)
