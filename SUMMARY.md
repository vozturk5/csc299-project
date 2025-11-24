Overview

This project implements a combined Personal Knowledge Management System (PKMS), a task management system with deadlines, priorities, tags, task editing, and deletion, a persistent JSON storage backend, a terminal-based chat interface, and an AI-powered note summarization feature using the OpenAI API.
Throughout development, I used multiple AI tools—OpenAI ChatGPT (web), Gemini (web), GitHub Copilot, VS Code Copilot Chat, and iterative prototypes—to plan, debug, and refine the software.

This summary describes my full development workflow, what worked well, what failed, and how I used AI models in complementary ways to reach the final result.

Planning and Early Prototypes

I started the project by reading the assignment carefully and writing down the main architecture:

PKMS for storing notes

Task manager with CRUD features

JSON state persistence

CLI chat interface

Optional AI “tools” or “agents”

Cross-platform Python code

My first prototypes were intentionally small. I created simple versions of add note, list notes, and basic task storage. This prototype wasn’t meant to be the final version—it was used only to explore how the interface should feel.

I used Gemini (web) at this stage to help brainstorm how PKMS tools work (e.g., Notion and Obsidian) and how tasks could be structured. Gemini was extremely good at broad, conceptual explanations and helped me think about tagging systems, priorities, and what kinds of features real PKMS applications include.

AI-Assisted Development Modes
1. ChatGPT (web / GPT-5.1 / GPT-5-mini)

This was my primary coding partner. I used ChatGPT in classic chat mode to:

debug exceptions

rewrite entire modules using EOF blocks

refactor directory structures

fix JSON serialization issues

repair imports

design prompts and structure for AI note summarization

explain OpenAI parameter issues (max_tokens vs. max_completion_tokens)

help me redesign the CLI interface

ChatGPT was the best tool for detailed debugging, step-by-step problem solving, and rewriting code reliably.

2. GitHub Copilot (auto-complete mode)

Inside VS Code, GitHub Copilot provided:

boilerplate code (function skeletons, JSON load/save patterns)

auto-completion for repeated patterns

quick helper suggestions for loops and dictionary handling

Copilot was strongest when expanding patterns I had already written.
It was not reliable for designing new functionality from scratch.

3. VS Code Copilot Chat

This was especially helpful for:

searching inside my own project files

explaining my own codebase line-by-line

suggesting refactors based on my directory structure

answering questions like “Where is this function called?”

helping diagnose mismatched return types

Copilot Chat acted more like a personal assistant inside my editor, giving context-aware explanations that ChatGPT (web) could not see.

4. Gemini (web)

I used Gemini during planning and during a few conceptual questions:

designing the tag system

thinking about how to structure the JSON

comparing different PKMS approaches

deciding between SQLite vs JSON

brainstorming what “AI agents” might mean in this project

Gemini was especially strong at high-level conceptual design and comparisons between tools.

What Worked Well
Layered prototypes

Building small prototypes first helped avoid large-scale rewrites. I threw away several prototypes before reaching the final structure.

Multi-AI workflow

Each AI tool had strengths:

ChatGPT → debugging + rewriting files

VS Code Copilot Chat → project structure analysis

GitHub Copilot → boilerplate generation

Gemini → conceptual design and brainstorming

Using them together created a smooth development pipeline.

Chat-style CLI

The chat interface allowed gradual feature additions without rewriting the UI each time. Every feature (search, tagging, deadlines, editing tasks) integrated naturally into the chat structure.

JSON persistence

Storing data in JSON kept everything simple and fully portable.

False Starts & What Didn’t Work
Advanced AI agents

I initially attempted:

AI task planning

Automatic tagging

Goal breakdown agents

But these repeatedly failed due to:

OpenAI parameter mismatches

response object structure confusion

streaming vs. non-streaming behavior

overly complex prompt patterns

Eventually, I kept only AI summarization of notes, which works reliably.

Task ID problems

Deleting tasks caused broken IDs early on.
I had to rewrite deletion logic to re-index the tasks list properly.

Copilot hallucinations

Sometimes Copilot invented nonexistent functions or APIs.
I learned to treat Copilot suggestions as “optional hints,” not authoritative code.

Parameter errors for AI models

gpt-5-mini only supports limited parameters.
Errors like:

“unsupported parameter: temperature”

“invalid parameter: max_tokens”

forced multiple rewrites of the summarization agent.

Final System Features

The final implementation includes:

Notes (PKMS)

add notes

list notes

search notes

AI summarize all notes

Tasks

add tasks (with title, tags, deadline, priority)

list tasks

search tasks (by text or tag)

mark tasks done

delete tasks

edit tasks (title, tags, deadline, priority)

Chat Interface

Runs entirely in the terminal and supports all commands via text-based chat.

Persistence

All state stored in JSON files inside data/.

Conclusion

This project was a full iterative development experience that combined:

software design

AI-driven coding

debugging

file rewriting

system architecture

user-interface creation

Using multiple AI tools together was the strongest part of the process. Each model (ChatGPT, Gemini, Copilot, VS Code Copilot Chat) contributed in a different way, and combining them produced a result far better than using only one.
