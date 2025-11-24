from pkms.documents import add_note, list_notes
from tasks.manager import add_task, list_tasks, search_tasks, mark_done, delete_task, edit_task
from pkms.search import search_notes
from agents.assistant import summarize_all_notes

def run_chat():
    print("=======================================")
    print("  FINAL PROJECT: PKMS + TASK MANAGER")
    print("      Chat-Style Command Line Interface")
    print("=======================================")
    print("Type 'help' to see all commands.\n")

    while True:
        cmd = input("> ").strip()

        if cmd == "help":
            print("Commands:")
            print("Tasks:")
            print("  add task <title> [#tag1 #tag2 ...]")
            print("  list tasks")
            print("  search tasks <query>")
            print("  done <id>")
            print("  delete task <id>")
            print("  edit task <id>")
            print("")
            print("Notes:")
            print("  add note <text>")
            print("  list notes")
            print("  search notes <query>")
            print("")
            print("AI Tools:")
            print("  ai summarize notes")
            print("")
            print("Other:")
            print("  exit")
            continue

        # ===== NOTES =====

        if cmd.startswith("add note "):
            text = cmd.replace("add note ", "").strip()
            note = add_note(text)
            print("Note added:", note)
            continue

        if cmd == "list notes":
            notes = list_notes()
            print("Notes:")
            for n in notes:
                if isinstance(n, dict):
                    print(f"[{n['id']}] {n['text']}")
                else:
                    print("⚠ Skipping invalid note entry:", n)
            continue

        if cmd.startswith("search notes "):
            q = cmd.replace("search notes ", "").strip()
            for r in search_notes(q):
                print("-", r)
            continue

        # ===== TASKS =====

        if cmd.startswith("add task "):
            title = cmd.replace("add task ", "").strip()

            deadline_input = input("Deadline (YYYY-MM-DD) or leave blank: ").strip()
            deadline = deadline_input if deadline_input else None

            priority_input = input("Priority [low/medium/high] default: medium: ").strip().lower()
            priority = priority_input if priority_input else "medium"

            task = add_task(title, priority=priority, deadline=deadline)
            print("Task added:", task)
            continue

        if cmd == "list tasks":
            tasks = list_tasks()
            print("Tasks:")
            for t in tasks:
                print(
                    f"[{t.get('id')}] {t.get('title')}  "
                    f"(done: {t.get('done', False)}, "
                    f"priority: {t.get('priority')}, "
                    f"deadline: {t.get('deadline')}, "
                    f"tags: {', '.join(t.get('tags', []))})"
                )
            continue

        if cmd.startswith("search tasks "):
            q = cmd.replace("search tasks ", "").strip()
            results = search_tasks(q)
            print("Search results:")
            for r in results:
                print(
                    f"[{r['id']}] {r['title']} "
                    f"(done: {r.get('done')}, priority: {r.get('priority')}, deadline: {r.get('deadline')})"
                )
            continue

        if cmd.startswith("done "):
            task_id = int(cmd.replace("done ", ""))
            result = mark_done(task_id)
            print("Marked as done:", result)
            continue

        if cmd.startswith("delete task "):
            task_id = int(cmd.replace("delete task ", ""))
            result = delete_task(task_id)
            if result:
                print(f"Task {task_id} deleted.")
            else:
                print("Task not found.")
            continue

        # ⭐ NEW: EDIT TASK
        if cmd.startswith("edit task "):
            task_id = int(cmd.replace("edit task ", ""))

            print("Leave blank to keep current value.")

            new_title = input("New title: ").strip()
            new_title = new_title if new_title else None

            new_deadline = input("New deadline (YYYY-MM-DD): ").strip()
            new_deadline = new_deadline if new_deadline else None

            new_priority = input("New priority [low/medium/high]: ").strip().lower()
            new_priority = new_priority if new_priority else None

            tag_input = input("New tags (#tag1 #tag2 ...) or blank: ").strip()
            if tag_input:
                tags = [t[1:] for t in tag_input.split() if t.startswith("#")]
            else:
                tags = None

            updated = edit_task(task_id, title=new_title, priority=new_priority,
                                deadline=new_deadline, tags=tags)

            if updated:
                print("Task updated:", updated)
            else:
                print("Task not found.")
            continue

        # ===== AI =====

        if cmd == "ai summarize notes":
            all_notes = list_notes()
            print("AI Summary:\n")
            print(summarize_all_notes(all_notes))
            continue

        if cmd == "exit":
            print("Goodbye!")
            break

        print("Unknown command. Type 'help'.")
