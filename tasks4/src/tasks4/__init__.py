from openai import OpenAI

def main() -> None:
    client = OpenAI()

    tasks = [
        """Develop a web-based calendar application that allows users to create,
        edit, and delete events. The system should send reminder notifications and
        synchronize with external calendars such as Google Calendar and Outlook.""",

        """Create a Python script that analyzes text files and extracts key
        statistics such as word count, most frequent words, and sentence complexity.
        The program should generate a concise summary of the document’s content."""
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} ---")
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes tasks into short phrases."},
                {"role": "user", "content": f"Summarize this task as a short phrase:\n{task}"}
            ],
        )
        summary = response.choices[0].message.content
        print("Summary:", summary)

if __name__ == "__main__":
    main()
