import json, sys
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).with_name("tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("Corrupted JSON, starting fresh.")
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def add_task(title):
    tasks = load_tasks()
    next_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({
        "id": next_id,
        "title": title,
        "done": False,
        "created": datetime.now().isoformat()
    })
    save_tasks(tasks)
    print(f"Added [{next_id}] {title}")

def list_tasks(show_all=True):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        status = "✅" if t.get("done") else "❌"
        print(f'[{t["id"]}] {status} {t["title"]} (created {t["created"]})')

def search_tasks(keyword):
    tasks = load_tasks()
    keyword = keyword.lower()
    matches = [t for t in tasks if keyword in t["title"].lower()]
    for t in matches:
        status = "✅" if t.get("done") else "❌"
        print(f'[{t["id"]}] {status} {t["title"]}')

def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Marked task [{task_id}] as done ✅")
            return
    print("Task not found.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task not found.")
    else:
        save_tasks(new_tasks)
        print(f"Deleted task [{task_id}]")

def main():
    if len(sys.argv) < 2:
        print("Usage: add|list|search|done|delete <args>")
        return
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "search" and len(sys.argv) > 2:
        search_tasks(" ".join(sys.argv[2:]))
    elif cmd == "done" and len(sys.argv) > 2:
        mark_done(int(sys.argv[2]))
    elif cmd == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    else:
        print("Invalid command or arguments.")

if __name__ == "__main__":
    main()
