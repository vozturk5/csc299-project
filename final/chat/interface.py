from pkms.documents import add_note, list_notes, save_notes, delete_note
from tasks.manager import (
    assign_note_to_task,
    unlink_task_from_notes,
    add_task,
    list_tasks,
    search_tasks,
    mark_done,
    delete_task,
    edit_task,
    sort_tasks,
    clear_completed_tasks
)
from pkms.search import search_notes
from agents.assistant import summarize_all_notes
from datetime import datetime, date

class C:
    HEADER = "\033[94m\033[1m"
    CMD = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"

def print_stats():
    tasks = list_tasks()
    notes = list_notes()

    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t.get("done"))
    overdue = 0
    due_today = 0
    due_week = 0

    today = date.today()

    for t in tasks:
        dl = t.get("deadline")
        if dl:
            try:
                d = date.fromisoformat(dl)
                if d < today:
                    overdue += 1
                elif d == today:
                    due_today += 1
                elif (d - today).days <= 7:
                    due_week += 1
            except:
                pass

    priorities = {"high": 0, "medium": 0, "low": 0}
    for t in tasks:
        p = t.get("priority", "medium")
        if p in priorities:
            priorities[p] += 1

    tag_counts = {}
    for t in tasks:
        for tag in t.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    linked_notes = sum(1 for n in notes if n.get("task_id"))

    print(C.HEADER + "====================================" + C.RESET)
    print(C.HEADER + "            PKMS STATS" + C.RESET)
    print(C.HEADER + "====================================" + C.RESET)

    print(f"{C.SUCCESS}Total tasks:{C.RESET} {total_tasks}")
    print(f"{C.SUCCESS}Completed:{C.RESET} {completed} ({ (completed/total_tasks*100) if total_tasks else 0:.0f}% )")
    print(f"{C.ERROR}Overdue:{C.RESET} {overdue}")
    print(f"{C.WARNING}Due Today:{C.RESET} {due_today}")
    print(f"{C.WARNING}Due This Week:{C.RESET} {due_week}")

    print("\n" + C.HEADER + "By Priority:" + C.RESET)
    for key, val in priorities.items():
        print(f"  {key.capitalize()}: {val}")

    print("\n" + C.HEADER + "By Tag:" + C.RESET)
    if tag_counts:
        for tag, count in tag_counts.items():
            print(f"  {tag}: {count}")
    else:
        print("  (No tags)")

    print("\n" + C.HEADER + "Notes:" + C.RESET)
    print(f"Total Notes: {len(notes)}")
    print(f"Notes Linked to Tasks: {linked_notes}")

    print(C.HEADER + "====================================" + C.RESET)


def run_chat():
    print(C.HEADER + "=======================================" + C.RESET)
    print(C.HEADER + "  FINAL PROJECT: PKMS + TASK MANAGER" + C.RESET)
    print(C.HEADER + "      Chat-Style Command Line Interface" + C.RESET)
    print(C.HEADER + "=======================================" + C.RESET)
    print(C.CMD + "Type 'help' to see all commands.\n" + C.RESET)

    while True:
        cmd = input(C.CMD + "> " + C.RESET).strip()

        if cmd == "help":
            print(C.HEADER + "Commands:" + C.RESET)
            print(C.CMD + "Tasks:" + C.RESET)
            print("  add task <title> [#tag1 #tag2 ...]")
            print("  list tasks  (--sort=deadline/priority/created)")
            print("  search tasks <query>")
            print("  done <id>")
            print("  delete task <id>")
            print("  edit task <id>")
            print("  clear done")

            print(C.CMD + "\nNotes:" + C.RESET)
            print("  add note <text>")
            print("  list notes")
            print("  delete note <id>")
            print("  search notes <query>")

            print(C.CMD + "\nStats:" + C.RESET)
            print("  stats  (view analytics dashboard)")

            print(C.CMD + "\nAI Tools:" + C.RESET)
            print("  ai summarize notes\n")

            print(C.CMD + "Other:" + C.RESET)
            print("  exit")
            continue

        # ===== NEW DELETE NOTE =====
        if cmd.startswith("delete note "):
            try:
                note_id = int(cmd.replace("delete note ", "").strip())
                result = delete_note(note_id)
                print(C.SUCCESS + "Note deleted." + C.RESET if result else C.ERROR + "Note not found." + C.RESET)
            except:
                print(C.ERROR + "Invalid note ID." + C.RESET)
            continue

        # ===== STATS =====
        if cmd == "stats":
            print_stats()
            continue

        # ===== NOTES =====
        if cmd.startswith("add note "):
            text = cmd.replace("add note ", "").strip()
            note = add_note(text)

            task_link = input(C.CMD + "Assign this note to a task ID (or leave blank): " + C.RESET).strip()
            if task_link.isdigit():
                assign_note_to_task(note["id"], int(task_link))

            print(C.SUCCESS + "Note added:" + C.RESET, note)
            continue

        if cmd == "list notes":
            notes = list_notes()
            print(C.HEADER + "Notes:" + C.RESET)
            for n in notes:
                task_info = C.WARNING + f" (task {n.get('task_id')})" + C.RESET if n.get("task_id") else ""
                print(f"{C.SUCCESS}[{n['id']}]{C.RESET} {n['text']}{task_info}")
            continue

        if cmd.startswith("search notes "):
            q = cmd.replace("search notes ", "").strip()
            results = search_notes(q)
            print(C.HEADER + "Search Results:" + C.RESET)
            for r in results:
                print("-", r)
            continue

        # ===== TASKS =====
        if cmd.startswith("add task "):
            title = cmd.replace("add task ", "").strip()

            deadline_input = input(C.CMD + "Deadline (YYYY-MM-DD) or leave blank: " + C.RESET).strip()
            deadline = deadline_input if deadline_input else None

            priority_input = input(C.CMD + "Priority [low/medium/high] default: medium: " + C.RESET).strip().lower()
            priority = priority_input if priority_input else "medium"

            task = add_task(title, priority=priority, deadline=deadline)
            print(C.SUCCESS + "Task added:" + C.RESET, task)
            continue

        if cmd.startswith("list tasks"):
            sort_method = None

            if "--sort=" in cmd:
                sort_method = cmd.split("--sort=")[1].strip()

            tasks = list_tasks()
            if sort_method:
                tasks = sort_tasks(tasks, sort_method)

            print(C.HEADER + "Tasks:" + C.RESET)
            notes = list_notes()
            for t in tasks:
                print(
                    f"{C.SUCCESS}[{t['id']}]{C.RESET} {t['title']} "
                    f"(done: {t['done']}, priority: {t.get('priority')}, deadline: {t.get('deadline')}) "
                    f"tags: {', '.join(t.get('tags', []))}"
                )

                linked = [n for n in notes if n.get("task_id") == t["id"]]
                if linked:
                    print(C.CMD + "   Notes:" + C.RESET)
                    for n in linked:
                        print(C.WARNING + f"      - ({n['id']}) {n['text']}" + C.RESET)

            continue

        if cmd == "clear done":
            removed = clear_completed_tasks()
            print(C.SUCCESS + "Completed tasks cleared." + C.RESET if removed else C.WARNING + "No completed tasks to clear." + C.RESET)
            continue

        if cmd.startswith("search tasks "):
            q = cmd.replace("search tasks ", "").strip()
            results = search_tasks(q)
            print(C.HEADER + "Search results:" + C.RESET)
            for r in results:
                print(
                    f"{C.SUCCESS}[{r['id']}]{C.RESET} {r['title']} "
                    f"(done: {r.get('done')}, priority: {r.get('priority')}, deadline: {r.get('deadline')})"
                )
            continue

        if cmd.startswith("done "):
            task_id = int(cmd.replace("done ", ""))
            result = mark_done(task_id)
            print(C.SUCCESS + "Marked as done:" + C.RESET, result)
            continue

        if cmd.startswith("delete task "):
            task_id = int(cmd.replace("delete task ", ""))
            result = delete_task(task_id)
            print(C.SUCCESS + "Task deleted." + C.RESET if result else C.ERROR + "Task not found." + C.RESET)
            continue

        if cmd.startswith("edit task "):
            task_id = int(cmd.replace("edit task ", "").strip())
            print(C.CMD + "Leave blank to keep current value." + C.RESET)

            new_title = input("New title: ").strip() or None
            new_deadline = input("New deadline (YYYY-MM-DD): ").strip() or None
            new_priority = input("New priority [low/medium/high]: ").strip().lower() or None

            tag_input = input("New tags (#tag1 #tag2 ...) or blank: ").strip()
            tags = [t[1:] for t in tag_input.split() if t.startswith("#")] if tag_input else None

            updated = edit_task(
                task_id,
                title=new_title,
                priority=new_priority,
                deadline=new_deadline,
                tags=tags
            )

            print(C.SUCCESS + "Task updated:" + C.RESET, updated if updated else C.ERROR + "Task not found." + C.RESET)
            continue

        # ===== AI =====
        if cmd == "ai summarize notes":
            all_notes = list_notes()
            print(C.HEADER + "AI Summary:\n" + C.RESET)
            print(summarize_all_notes(all_notes))
            continue

        if cmd == "exit":
            print(C.SUCCESS + "Goodbye!" + C.RESET)
            break

        print(C.ERROR + "Unknown command. Type 'help'." + C.RESET)
