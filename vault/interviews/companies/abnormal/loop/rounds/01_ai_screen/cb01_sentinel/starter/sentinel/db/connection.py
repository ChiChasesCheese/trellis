from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open a sqlite connection with Row access and foreign keys on."""
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
