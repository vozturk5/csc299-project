from openai import OpenAI
client = OpenAI()

def summarize_all_notes(notes):
    """
    Summarize all valid notes (dict entries only).
    """

    # Filter out invalid entries (strings, corrupted entries)
    clean = []
    for n in notes:
        if isinstance(n, dict) and "id" in n and "text" in n:
            clean.append(n)

    if not clean:
        return "No valid notes to summarize."

    # Combine notes into one block of text
    joined_text = "\n".join([f"{n['id']}. {n['text']}" for n in clean])

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize these notes concisely:\n\n{joined_text}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"

