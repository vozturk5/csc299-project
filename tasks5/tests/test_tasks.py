import os
import tempfile
import json

from tasks import add_task, list_tasks, search_tasks, save_tasks


def test_add_and_list():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        # start empty
        save_tasks([], db_path=path)
        t1 = add_task("Buy milk", "2L", ["shopping"], db_path=path)
        t2 = add_task("Call Bob", "On Tuesday", ["phone"], db_path=path)
        tasks = list_tasks(db_path=path)
        assert any(t["title"] == "Buy milk" for t in tasks)
        assert any(t["title"] == "Call Bob" for t in tasks)
        assert t1["id"] != t2["id"]
    finally:
        os.remove(path)


def test_search():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        save_tasks([
            {"id": 1, "title": "Buy milk", "description": "2L", "tags": ["shopping"]},
            {"id": 2, "title": "Prepare report", "description": "Financial Q3", "tags": ["work"]}
        ], db_path=path)
        res = search_tasks("milk", db_path=path)
        assert len(res) == 1 and res[0]["title"] == "Buy milk"
        res2 = search_tasks("work", db_path=path)
        assert len(res2) == 1 and res2[0]["title"] == "Prepare report"
        res3 = search_tasks("nomatch", db_path=path)
        assert len(res3) == 0
    finally:
        os.remove(path)
