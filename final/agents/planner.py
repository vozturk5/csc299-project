from openai import OpenAI

# Your API key:
client = OpenAI(api_key="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")

def suggest_plan(tasks: list) -> str:
    """
    Sends task data to GPT-5-mini and returns a recommended plan.
    """
    if not tasks:
        return "You have no tasks. Nothing to plan!"

    # Format tasks for the prompt
    formatted = "\n".join(
        f"- (id: {t['id']}) {t['title']} | done={t['done']} | tags={t.get('tags', [])}"
        for t in tasks
    )

    prompt = f"""
You are an intelligent productivity agent. The user has the following tasks:

{formatted}

Your job:
1. Analyze task urgency.
2. Recommend what task the user should do next.
3. Give a very short explanation.
Respond with ONLY one recommended task and the explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are a helpful planning assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
        )

        answer = response.choices[0].message["content"]
        return answer.strip()

    except Exception as e:
        return f"[AI ERROR] {e}"
