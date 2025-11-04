# Task 2 – Enhanced JSON Task CLI

This version expands the Task 1 command-line app with **mark-as-done**, **delete**, and improved task management features.  
It demonstrates how small, iterative development steps lead to a more capable and realistic productivity tool.

---

## ⚙️ Requirements
- Python 3.8 or higher  
- No third-party libraries required (pure Python)  
- Works on Windows, macOS, and Linux  

---

## 🚀 How to Use

### 📝 Add new tasks  
```bash
python task_cli.py add "Finish Task 2"
python task_cli.py add "Submit PKMS project"  
```

Each task is stored automatically in `tasks.json`.

---

### 📋 List tasks  
```bash
python task_cli.py list  
```

Displays all current tasks with checkmarks for status:  
[1] ❌ Finish Task 2 (created 2025-11-03T15:10:00)  
[2] ❌ Submit PKMS project (created 2025-11-03T15:12:20)  

---

### 🔍 Search tasks  
```bash
python task_cli.py search PKMS  
```

Finds any task containing a keyword:  
[2] ❌ Submit PKMS project  

---

### ✅ Mark tasks as done  
```bash
python task_cli.py done 1  
```

Output:  
Task [1] marked as done ✅  

---

### 🗑️ Delete tasks  
```bash
python task_cli.py delete 2  
```

Output:  
Deleted task [2]  

---

## 📄 Example Data File  
After running commands, your `tasks.json` will look like:
```bash
[
  {
    "id": 1,
    "title": "Finish Task 2",
    "done": true,
    "created": "2025-11-03T15:10:00"
  }
]
```

---

## 🧠 Summary
| Command | Description |
|----------|--------------|
| add | Add a new task |
| list | Display all tasks |
| search | Search tasks by keyword |
| done | Mark task as complete |
| delete | Remove task by ID |

This marks your second development milestone in CSC299, showing progress toward a complete **Personal Knowledge and Task Management System (PKMS)**.
