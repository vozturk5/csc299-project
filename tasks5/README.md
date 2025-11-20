# Simple Tasks Manager

A tiny Python CLI to add, list, and search tasks stored in a JSON file. This project uses Typer for the CLI.

Usage:

- Add a task:

  python tasks.py add "Buy milk" --desc "2 liters" --tags shopping,errands

- List tasks:

  python tasks.py list

- Search:

  python tasks.py search milk

By default tasks are stored in `tasks.json` next to `tasks.py`. Use `--db` to point to a different file.

This project includes a small test suite using `pytest`.
