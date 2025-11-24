import os
from openai import OpenAI

# Load the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-5-mini"


def ai_plan(tasks: list) -> str:
    """
    Takes a list of tasks and returns one recommended next action.
    """
    prompt = f"""
You are an intelligent task-planning agent.
Given the user's task list below, choose ONE task that is the best next action.

TASK LIST:
{tasks}

Respond with ONLY the task title.
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=100,
    )

    return response.output_text.strip()


def ai_summarize_notes(notes: list) -> str:
    """
    Summarize all notes into a short paragraph.
    """
    prompt = f"""
Summarize the following notes into a clear, simple paragraph.

NOTES:
{notes}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=150,
    )

    return response.output_text.strip()


def ai_autotag(task_title: str) -> list:
    """
    Generate tags for a task title.
    """
    prompt = f"""
Generate simple one-word tags for this task title.

TASK:
"{task_title}"

Respond in JSON list format, for example:
["home", "urgent"]
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=50,
    )

    text = response.output_text.strip()

    try:
        return eval(text)
    except:
        return []


def ai_break_goal(goal: str) -> list:
    """
    Break a big goal into 3–6 smaller tasks.
    """
    prompt = f"""
Break down the following big goal into 3 to 6 small actionable steps.

GOAL:
"{goal}"

Respond in JSON list format, example:
["step 1", "step 2", "step 3"]
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=150,
    )

    text = response.output_text.strip()

    try:
        return eval(text)
    except:
        return []


def ai_chat(message: str) -> str:
    """
    Free-form chat with the AI assistant.
    """
    response = client.responses.create(
        model=MODEL,
        input=message,
        max_output_tokens=200,
    )

    return response.output_text.strip()
