"""sqlite plumbing: connect, and apply ``migrations/NNNN_name.sql`` files in order.

Applied versions live in the schema_migrations table.
"""
from __future__ import annotations

import logging
import sqlite3
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


class _Result:
    """Rows fetched while the connection lock was held, with the cursor attributes we use."""

    def __init__(self, rows: list[sqlite3.Row], rowcount: int, lastrowid: int | None):
        self._rows, self.rowcount, self.lastrowid = rows, rowcount, lastrowid

    def fetchone(self) -> sqlite3.Row | None:
        return self._rows[0] if self._rows else None

    def fetchall(self) -> list[sqlite3.Row]:
        return list(self._rows)

    def __iter__(self) -> Iterator[sqlite3.Row]:
        return iter(self._rows)


class LockedConnection(sqlite3.Connection):
    """One connection shared by the API's worker threads: every statement runs under a lock.

    sqlite3 reuses prepared statements across cursors, so two threads running the same SQL on
    one connection corrupt each other. Statements are serialised; sequences of statements are not,
    so callers still need constraints, not just reads, to stay correct under concurrency.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._lock = threading.RLock()

    def execute(self, sql: str, parameters: Any = ()) -> _Result:  # type: ignore[override]
        with self._lock:
            cur = super().execute(sql, parameters)
            return _Result(cur.fetchall(), cur.rowcount, cur.lastrowid)

    def executescript(self, script: str) -> Any:  # type: ignore[override]
        with self._lock:
            return super().executescript(script)

    def commit(self) -> None:
        with self._lock:
            super().commit()


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open a sqlite connection with Row access and foreign keys on."""
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False, factory=LockedConnection)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection, directory: Path = MIGRATIONS_DIR) -> list[str]:
    """Apply pending migrations; returns the versions applied by this call."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations "
        "(version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
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
