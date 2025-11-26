import json
import os
from datetime import datetime

DATA_FILE = "data/notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def _normalize_notes(raw_notes):
    cleaned = []
    next_id = 1

    for n in raw_notes:
        if isinstance(n, dict) and "text" in n:
            text = str(n["text"])

            try:
                nid = int(n.get("id", next_id))
            except:
                nid = next_id

            created = n.get("created")
            if not created:
                created = datetime.now().isoformat()

            task_id = n.get("task_id", None)

            cleaned.append({
                "id": nid,
                "text": text,
                "created": created,
                "task_id": task_id
            })

            next_id = max(next_id, nid + 1)

    for i, n in enumerate(cleaned, start=1):
        n["id"] = i

    return cleaned

def add_note(text, task_id=None):
    raw = load_notes()
    notes = _normalize_notes(raw)

    new_id = len(notes) + 1

    note = {
        "id": new_id,
        "text": text,
        "created": datetime.now().isoformat(),
        "task_id": task_id
    }

    notes.append(note)
    save_notes(notes)
    return note

def list_notes(order=None):
    raw = load_notes()
    notes = _normalize_notes(raw)

    if notes != raw:
        save_notes(notes)

    if order == "newest":
        notes.sort(key=lambda n: n["created"], reverse=True)
    elif order == "oldest":
        notes.sort(key=lambda n: n["created"])

    return notes

def search_notes(query):
    q = query.lower()
    notes = list_notes()
    return [n for n in notes if q in n["text"].lower()]

def assign_note_to_task(note_id, task_id):
    notes = list_notes()
    for n in notes:
        if n["id"] == note_id:
            n["task_id"] = task_id
            save_notes(notes)
            return True
    return False

def unlink_task_from_notes(task_id):
    notes = list_notes()
    changed = False
    for n in notes:
        if n.get("task_id") == task_id:
            n["task_id"] = None
            changed = True
    if changed:
        save_notes(notes)
    return changed

# ============================================
# NEW: DELETE NOTE
# ============================================
def delete_note(note_id):
    notes = list_notes()
    new_notes = [n for n in notes if n["id"] != note_id]

    if len(new_notes) == len(notes):
        return False

    # Reassign IDs
    for i, n in enumerate(new_notes, start=1):
        n["id"] = i

    save_notes(new_notes)
    return True
