import json
import os
from pkms.documents import assign_note_to_task, unlink_task_from_notes

DATA_FILE = "data/tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def clear_completed_tasks():
    tasks = load_tasks()
    new_tasks = [t for t in tasks if not t.get("done", False)]
    if len(new_tasks) == len(tasks):
        return 0
    for i, t in enumerate(new_tasks, start=1):
        t["id"] = i
    save_tasks(new_tasks)
    return 1

def add_task(title, priority="medium", deadline=None):
    tasks = load_tasks()
    new_id = len(tasks) + 1

    tags = []
    parts = title.split()
    pure_title_parts = []
    for p in parts:
        if p.startswith("#"):
            tags.append(p[1:].lower())
        else:
            pure_title_parts.append(p)
    final_title = " ".join(pure_title_parts)

    task = {
        "id": new_id,
        "title": final_title,
        "done": False,
        "priority": priority,
        "deadline": deadline,
        "tags": tags,
        "notes": []
    }

    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks():
    return load_tasks()

def search_tasks(query):
    tasks = load_tasks()
    q = query.lower()
    if q.startswith("#"):
        tag = q[1:]
        return [t for t in tasks if tag in t.get("tags", [])]
    return [t for t in tasks if q in t["title"].lower()]

def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            return t
    return None

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return None

    unlink_task_from_notes(task_id)

    for i, t in enumerate(new_tasks, start=1):
        t["id"] = i

    save_tasks(new_tasks)
    return True

def edit_task(task_id, title=None, priority=None, deadline=None, tags=None):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if title is not None:
                t["title"] = title
            if priority is not None:
                t["priority"] = priority
            if deadline is not None:
                t["deadline"] = deadline
            if tags is not None:
                t["tags"] = tags
            save_tasks(tasks)
            return t
    return None

def add_note_to_task(task_id, note_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if "notes" not in t:
                t["notes"] = []
            if note_id not in t["notes"]:
                t["notes"].append(note_id)
            save_tasks(tasks)
            return True
    return False

def sort_tasks(tasks, method):
    if method == "created":
        return sorted(tasks, key=lambda t: t["id"])
    if method == "priority":
        order = {"high": 1, "medium": 2, "low": 3}
        return sorted(tasks, key=lambda t: order.get(t["priority"], 99))
    if method == "deadline":
        return sorted(tasks, key=lambda t: (t["deadline"] is None, t["deadline"]))
    return tasks
