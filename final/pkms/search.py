from .storage import load_notes

def search_notes(query: str):
    notes = load_notes()
    return [n for n in notes if query.lower() in n.lower()]
