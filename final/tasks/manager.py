import json
import os

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
        "tags": tags
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

    for i, t in enumerate(new_tasks, start=1):
        t["id"] = i

    save_tasks(new_tasks)
    return True


# ⭐ NEW: EDIT TASK
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
