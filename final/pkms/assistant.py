from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY_HERE")  # replace with your key


def summarize_selected_notes(note_texts):
    """
    note_texts = list of plain text notes selected by the user.
    """
    combined = "\n\n".join(f"- {n}" for n in note_texts)

    prompt = (
        "Summarize the following notes in a short, clear paragraph:\n\n"
        f"{combined}\n\nSummary:"
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes notes."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=200
    )

    return response.choices[0].message["content"]


def ai_plan(tasks):
    """
    Suggest what to do next based on tasks.
    """
    task_list = "\n".join(
        f"- {t['title']} (done: {t['done']})" for t in tasks
    )

    prompt = (
        "Here are my tasks:\n"
        f"{task_list}\n\n"
        "Based on these tasks, what should I do next? Answer briefly."
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a productivity assistant."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=150
    )

    return response.choices[0].message["content"]


def ai_chat(message):
    """
    Free-form chat with the assistant.
    """
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant."},
            {"role": "user", "content": message}
        ],
        max_completion_tokens=200
    )

    return response.choices[0].message["content"]
