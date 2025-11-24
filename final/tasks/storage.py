import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tasks.json")

def load_tasks():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_PATH, "w") as f:
        json.dump(tasks, f, indent=2)
