# Development Summary for PKMS + Task Manager Project

This document explains, in detail, the full development process of my Personal Knowledge Management System (PKMS) + Task Manager project, including all tools, AI-assistant modes, tests, planning steps, and false starts.

---

## 1. Overview of My Development Process

I approached this project by treating it as a real software engineering workflow. Instead of coding everything at once, I iterated through multiple prototypes, gradually expanding features such as task creation, notes, AI integration, tagging, sorting, linkage between notes and tasks, and a full analytics dashboard.

A key part of the process was using **multiple AI-coding assistance modes simultaneously**, comparing their strengths and weaknesses.

---

## 2. AI Systems and Tools Used

### **2.1 ChatGPT (Chat Interface)**
I used ChatGPT as my primary conversational coding assistant.  
I used it in several distinct modes:

- **ChatGPT 5.1 (regular mode)** — for brainstorming, debugging errors, rewriting functions, and adding new features.
- **ChatGPT Code Mode** — for step-by-step debugging and multi-file refactoring.
- **ChatGPT Terminal Simulation** — to generate correct CLI flows, input/output behavior, and test interaction examples.

Most structural refactoring, JSON consistency checks, and logic validation were done here.

---

### **2.2 GitHub Copilot**
I used **three different modes of Copilot**:

- **Copilot Inline Suggestions**  
  Helped autofill repetitive patterns (like JSON field updates, print formatting).
- **Copilot Chat (VS Code)**  
  Used to generate test prototypes, code explanations, and quick documentation.
- **Copilot “Fix This” mode**  
  Used to attempt bug fixes directly inside VS Code, especially when dealing with tasks.json and data normalization issues.

Copilot was fast for generating boilerplate but not reliable for multi-file logic.

---

### **2.3 Google Gemini Advanced**
I also used Gemini in the browser for:

- sanity-checking JSON formats  
- validating that the CLI logic was consistent  
- generating backup versions of functions before replacing anything  
- helping with edge cases (sorting, deadline comparisons)

Gemini provided alternate solutions that I compared against ChatGPT suggestions.

---

### **2.4 Manual Planning Artifacts**
I created multiple planning steps:

- **Feature List Draft** – everything required for PKMS + Tasks + AI.
- **Command Table** – listing all CLI commands and their expected input/output.
- **Data Model Specification** – fields for tasks, notes, timestamps, linking, etc.
- **Incremental Build Plan** – add notes → add sorting → add tagging → add linking → add stats, etc.

These “documents” guided the direction of development and prevented accidental overwriting.

---

## 3. Testing Strategy

### **3.1 Attempted Automated Testing**
I generated pytest tests with GitHub Copilot:

- test_add_task()  
- test_search_tasks()  
- test_tag_filtering()  
- test_note_assignment()

However:

- The tests kept failing due to data mutation across tests.
- Fixtures constantly conflicted with JSON files.
- Mocking file I/O became too unstable.

Because of this, **I deleted the tests** and switched to manual testing.

### **3.2 Manual Testing**
I manually tested every feature in the terminal:

- Adding/editing/deleting tasks  
- Searching tasks by text and tags  
- Sorting by priority, deadline, and creation order  
- Adding notes, linking notes, unlinking notes  
- Stats dashboard outputs  
- AI summarization  
- Edge cases (empty lists, invalid IDs, corrupted JSON)

Manual testing ensured real behavior matched expectations.

---

## 4. What Worked Very Well

- Using ChatGPT for multi-file coordination.
- Incremental feature expansion, one layer at a time.
- Using Copilot inline suggestions for repetitive refactors.
- Designing the JSON schema early.
- The modular architecture (pkms/, tasks/, chat/, agents/) stayed stable.

---

## 5. What Did NOT Work / False Starts

- Copilot-generated tests repeatedly broke the project.
- Early versions of tasks.json became corrupted and required normalization code.
- Original AI integration leaked an OpenAI API key (fixed later).
- I initially tried adding Neo4J support but abandoned it due to time constraints.
- I tried linking tasks → notes using titles instead of IDs, which caused conflicts.

These failures helped improve the final architecture.

---

## 6. Final Result

The final software is the product of:

- AI-assisted planning  
- iterative prototyping  
- multi-agent coding support  
- careful refactoring  
- manual validation  

The final version includes:

- Full PKMS note system with timestamps
- Robust task manager with tagging, priorities, deadlines, sorting
- Two-way linking between notes and tasks
- AI summarization tools
- A fully colored CLI interface
- Analytics Dashboard (overdue tasks, tag frequency, priority distribution)

This workflow reflects a real-world development lifecycle enhanced by modern AI tools.

---

