from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", ".pytest_cache", "__pycache__", "logs"}
SKIP_FILES = {".env", "devspace_bot.db"}
TOKEN_RE = re.compile(r"\b\d{8,}:[A-Za-z0-9_-]{20,}\b")
WEAK_SECRET_RE = re.compile(
    r"(?m)^(BOT_TOKEN=\d+:|MYSQL_(?:ROOT_)?PASSWORD=(?:change|strong)_\w+)"
)


def iter_public_files():
    for path in ROOT.rglob("*"):
        relative_parts = set(path.relative_to(ROOT).parts)
        if path.is_dir() or relative_parts & SKIP_DIRS or path.name in SKIP_FILES:
            continue
        yield path


def main() -> int:
    failures: list[str] = []
    for path in iter_public_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if TOKEN_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)} contains a Telegram-like token")

        if WEAK_SECRET_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)} contains a weak example secret")

    if failures:
        print("Public push check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Public push check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
