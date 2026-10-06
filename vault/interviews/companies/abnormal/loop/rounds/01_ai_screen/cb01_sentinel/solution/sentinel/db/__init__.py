"""sqlite plumbing: connect, and apply ``migrations/NNNN_name.sql`` files in order.

Applied versions live in the schema_migrations table.
"""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from sentinel.db.repositories import EventRepository

log = logging.getLogger(__name__)

def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open a sqlite connection with Row access and foreign keys on."""
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def migrate(conn: sqlite3.Connection, directory: Path = MIGRATIONS_DIR) -> list[str]:
    """Apply pending migrations; returns the versions applied by this call."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    done = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}
    applied: list[str] = []
    for path in sorted(directory.glob("[0-9][0-9][0-9][0-9]_*.sql")):
        version = path.stem
        if version in done:
            continue
        log.info("applying migration %s", version)
        conn.executescript(path.read_text())
        conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))
        conn.commit()
        applied.append(version)
    return applied


__all__ = ["EventRepository", "connect", "migrate"]
