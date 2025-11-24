import json
import os

DATA_FILE = "data/notes.json"


def load_notes():
    """Load raw notes from disk (may contain old/bad entries)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # If the file is corrupted, start fresh
        return []


def save_notes(notes):
    """Save notes list back to disk."""
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def _normalize_notes(raw_notes):
    """
    Take whatever is in the JSON file and return a clean list
    of dicts: {"id": int, "text": str}.
    Any non-dict / malformed entries are discarded.
    """
    cleaned = []
    next_id = 1
    for n in raw_notes:
        if isinstance(n, dict) and "text" in n:
            text = str(n["text"])
            # use existing id if it is an int, otherwise reassign
            try:
                nid = int(n.get("id", next_id))
            except Exception:
                nid = next_id
            cleaned.append({"id": nid, "text": text})
            next_id = max(next_id, nid + 1)
    # re-assign sequential ids to be safe and consistent
    for i, n in enumerate(cleaned, start=1):
        n["id"] = i
    return cleaned


def add_note(text):
    """
    Add a new note with an integer id and given text.
    """
    raw = load_notes()
    notes = _normalize_notes(raw)
    new_id = len(notes) + 1
    note = {
        "id": new_id,
        "text": text,
    }
    notes.append(note)
    save_notes(notes)
    return note


def list_notes():
    """
    Return a cleaned list of note dicts.
    Also rewrites the JSON file in normalized form the first time.
    """
    raw = load_notes()
    notes = _normalize_notes(raw)
    # if normalization changed anything, persist it
    if notes != raw:
        save_notes(notes)
    return notes


def search_notes(query):
    """
    Case-insensitive search over note text.
    """
    notes = list_notes()
    q = query.lower()
    return [n for n in notes if q in n["text"].lower()]
