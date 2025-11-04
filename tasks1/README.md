# Task 1 – JSON Task CLI

A prototype command-line Task Manager that allows you to **store**, **list**, and **search** tasks using a simple JSON data file.

---

## 📁 Project Overview
This is a minimal, portable Python CLI application developed for the CSC299 project.  
It demonstrates how to save, view, and search tasks without a database — all data is stored locally in `tasks.json`.

---

## ⚙️ Requirements
- Python 3.8 or newer  
- Works on Windows, macOS, or Linux  
- Uses only Python’s built-in libraries (no installs required)

---

## 🚀 How to Run
From inside the `tasks1` directory, run the following commands in **PowerShell** or any terminal.

### 📝 Store a new task
Use the `add` command to store (save) a new task:
```bash
python task_cli.py add "Read PKMS paper"
python task_cli.py add "Write study reflection"
```

### 📋 List all tasks
Use the list command to view every stored task:
```bash
python task_cli.py list
```

### 🔍 Search for tasks
Use the search command to find tasks by keyword:
```bash
python task_cli.py search PKMS
```

### 📄 Data Storage
After adding tasks, a tasks.json file is automatically created in the same folder.


---


## 🧠 Summary
add → stores a task
list → displays all tasks
search → finds tasks by keyword
Data is stored persistently in tasks.json
This completes Task 1, demonstrating a working prototype CLI app for storing, listing, and searching tasks.

