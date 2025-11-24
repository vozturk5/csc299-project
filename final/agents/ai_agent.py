"""
AI-powered agents for the final project.

This module uses the OpenAI API to:
- Plan which task the user should do next
- Summarize all notes
- Generate a daily report

Requires environment variables:
  OPENAI_API_KEY=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
  OPENAI_MODEL=gpt-5-mini  (or whichever model you use)
"""

from __future__ import annotations
import os
from typing import Any, Dict, List
from openai import OpenAI

# Create OpenAI client (reads OPENAI_API_KEY automatically)
_client = OpenAI()

# Use your model (default = gpt-5-mini)
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


def _format_tasks(tasks: List[Dict[str, Any]]) -> str:
    lines = []
    for t in tasks:
        tid = t.get("id", "?")
        title = t.get("title", "(no title)")
        done = t.get("done", False)
        tags = ", ".join(t.get("tags", [])) or "none"
        status = "done" if done else "not done"
        lines.append(f"- #{tid}: {title} [tags: {tags}] ({status})")
    return "\n".join(lines)


def _format_notes(notes: List[Any]) -> str:
    result = []
    for n in notes:
        if isinstance(n, dict):
            text = n.get("text") or n.get("content") or str(n)
        else:
            text = str(n)
        result.append(f"- {text}")
    return "\n".join(result)


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        response = _client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",    "content": user_prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    except Exception as exc:
        return f"[AI error: {exc}]"


# ---------- PUBLIC AGENT FUNCTIONS ----------

def plan_with_ai(tasks: List[Dict[str, Any]]) -> str:
    if not tasks:
        return "No tasks available — add one using 'add task <title>'."

    block = _format_tasks(tasks)

    system = (
        "You are an intelligent productivity coach. "
        "Recommend the most important next task."
    )

    user = (
        "Here are my tasks:\n"
        f"{block}\n\n"
        "Pick the ONE most important task I should do next. "
        "Explain your reasoning in 2–4 sentences."
    )

    return _call_llm(system, user)


def summarize_notes_with_ai(notes: List[Any]) -> str:
    if not notes:
        return "No notes yet — add one using 'add note <text>'."

    block = _format_notes(notes)

    system = (
        "You are a study assistant. Summarize notes concisely and clearly."
    )

    user = (
        "Here are my notes:\n"
        f"{block}\n\n"
        "Write a 5–7 sentence summary capturing key points."
    )

    return _call_llm(system, user)


def daily_report_with_ai(tasks: List[Dict[str, Any]], notes: List[Any]) -> str:
    tasks_block = _format_tasks(tasks) if tasks else "None"
    notes_block = _format_notes(notes) if notes else "None"

    system = (
        "You are a helpful assistant generating a daily report for a student."
    )

    user = (
        "Here is today's data.\n\n"
        "Tasks:\n"
        f"{tasks_block}\n\n"
        "Notes:\n"
        f"{notes_block}\n\n"
        "Write a short daily report including:\n"
        "- What seems done today\n"
        "- What remains urgent\n"
        "- 2–3 suggestions for tomorrow\n"
        "Keep under 10 sentences."
    )

    return _call_llm(system, user)
