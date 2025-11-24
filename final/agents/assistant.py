import os
from openai import OpenAI

def summarize_all_notes(notes):
    """
    Summarizes all notes using GPT-5-mini (or any model you choose).
    Requires OPENAI_API_KEY to be set in environment variables.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "AI Error: No API key found. Please set OPENAI_API_KEY environment variable."

    client = OpenAI(api_key=api_key)

    if not notes:
        return "There are no notes to summarize."

    joined = "\n".join([f"[{n['id']}] {n['text']}" for n in notes])

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "user", "content": f"Summarize the following notes:\n{joined}"}
            ],
            max_completion_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: Could not read response.\n{e}"
