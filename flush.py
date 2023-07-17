import os
import shutil
from pathlib import Path

from typing import Callable, List

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def flush(dir: Path, search: str, worker: Callable[[Path], None]):
    for folder in os.listdir(dir):
        path = dir / folder

        if search in str(path):
            worker(path)
        elif os.path.isdir(path):
            flush(path, search, worker)


flush(BASE_DIR, "__pycache__", lambda dir: shutil.rmtree(dir))


def depthDelete(dir: Path, excludes: List[str]):
    for file in os.listdir(dir):
        if file not in excludes:
            os.remove(dir / file)


flush(BASE_DIR, "migrations", lambda dir: depthDelete(dir, ["__init__.py"]))

dbPath = BASE_DIR / "db.sqlite3"

if os.path.exists(dbPath):
    os.remove(dbPath)

