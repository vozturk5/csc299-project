"""Simple task manager CLI: add, list, search tasks stored in a JSON file.

Usage examples (from project root):
  python tasks.py add "Buy milk" --desc "2 liters" --tags shopping,errands
  python tasks.py list
  python tasks.py search milk
"""
import json
import os
from typing import List, Dict, Any, Optional


DEFAULT_DB = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks(db_path: str = DEFAULT_DB) -> List[Dict[str, Any]]:
    if not os.path.exists(db_path):
        return []
    with open(db_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks: List[Dict[str, Any]], db_path: str = DEFAULT_DB) -> None:
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(title: str, description: Optional[str] = None, tags: Optional[List[str]] = None, db_path: str = DEFAULT_DB) -> Dict[str, Any]:
    tasks = load_tasks(db_path)
    new_id = max((t.get("id", 0) for t in tasks), default=0) + 1
    task = {
        "id": new_id,
        "title": title,
        "description": description or "",
        "tags": tags or []
    }
    tasks.append(task)
    save_tasks(tasks, db_path)
    return task


def list_tasks(db_path: str = DEFAULT_DB) -> List[Dict[str, Any]]:
    return load_tasks(db_path)


def search_tasks(query: str, db_path: str = DEFAULT_DB) -> List[Dict[str, Any]]:
    q = query.lower()
    results = []
    for t in load_tasks(db_path):
        if q in t.get("title", "").lower() or q in t.get("description", "").lower() or any(q in tag.lower() for tag in t.get("tags", [])):
            results.append(t)
    return results


def _print_task(t: Dict[str, Any]) -> None:
    tags = ", ".join(t.get("tags", []))
    print(f"[{t['id']}] {t['title']}" + (f" - {t['description']}" if t.get("description") else "") + (f" (tags: {tags})" if tags else ""))


def _create_cli_app() -> object:
    """Create and return a Typer app. Imported lazily so module import (for tests) doesn't require Typer.

    Return type is object to avoid typing dependency at module import time.
    """
    import typer as _typer

    _app = _typer.Typer(help="Simple task manager: add, list, search tasks stored in a JSON file")

    @_app.command("add")
    def _cli_add(title: str = _typer.Argument(..., help="Task title"),
                 desc: str = _typer.Option("", "--desc", "-d", help="Description"),
                 tags: str = _typer.Option("", "--tags", "-t", help="Comma-separated tags"),
                 db: str = _typer.Option(DEFAULT_DB, "--db", help="Path to task DB file")) -> None:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        task = add_task(title, desc, tag_list, db_path=db)
        _typer.echo("Added:")
        _print_task(task)

    @_app.command("list")
    def _cli_list(db: str = _typer.Option(DEFAULT_DB, "--db", help="Path to task DB file")) -> None:
        tasks = list_tasks(db_path=db)
        if not tasks:
            _typer.echo("(no tasks)")
            raise _typer.Exit()
        for t in tasks:
            _print_task(t)

    @_app.command("search")
    def _cli_search(query: str = _typer.Argument(..., help="Search query"),
                    db: str = _typer.Option(DEFAULT_DB, "--db", help="Path to task DB file")) -> None:
        results = search_tasks(query, db_path=db)
        if not results:
            _typer.echo("(no matches)")
            raise _typer.Exit()
        for t in results:
            _print_task(t)

    return _app


def main(argv: Optional[List[str]] = None) -> None:
    """Run the CLI; kept for compatibility with previous entrypoints.

    If argv is provided, pass it to Typer's app invocation.
    """
    _app = _create_cli_app()
    if argv is None:
        _app()
    else:
        _app(argv)


if __name__ == "__main__":
    main()
