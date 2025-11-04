import json, sys
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).with_name("tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def add_task(title):
    tasks = load_tasks()
    next_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": next_id, "title": title, "created": datetime.now().isoformat()})
    save_tasks(tasks)
    print(f"Added [{next_id}] {title}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        print(f'[{t["id"]}] {t["title"]} ({t["created"]})')

def search_tasks(keyword):
    tasks = load_tasks()
    keyword = keyword.lower()
    matches = [t for t in tasks if keyword in t["title"].lower()]
    for t in matches:
        print(f'[{t["id"]}] {t["title"]}')

def main():
    if len(sys.argv) < 2:
        print("Usage: add|list|search")
        return
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 3:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "search" and len(sys.argv) >= 3:
        search_tasks(" ".join(sys.argv[2:]))
    else:
        print("Invalid command.")
if __name__ == "__main__":
    main()
