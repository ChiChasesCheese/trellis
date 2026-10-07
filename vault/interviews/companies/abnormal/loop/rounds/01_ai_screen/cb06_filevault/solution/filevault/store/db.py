"""sqlite access: one connection per thread, migrations, and the ``transaction()`` helper."""
from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


class Database:
    """Connections are created lazily per thread (``conn``) and run in autocommit mode.

    Writes that must be atomic together go through ``transaction()``, which takes sqlite's write
    lock up front (``BEGIN IMMEDIATE``) so concurrent writers queue instead of deadlocking.
    """

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self._local = threading.local()
        self._opened: list[sqlite3.Connection] = []
        self._lock = threading.Lock()

    @property
    def conn(self) -> sqlite3.Connection:
        conn: sqlite3.Connection | None = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.path, isolation_level=None, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout = 5000")
            conn.execute("PRAGMA foreign_keys = ON")
            self._local.conn = conn
            with self._lock:
                self._opened.append(conn)
        return conn

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """``BEGIN IMMEDIATE`` ... ``COMMIT``; rolls back if the block raises."""
        conn = self.conn
        if conn.in_transaction:
            raise RuntimeError("transactions do not nest")
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield conn
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        conn.execute("COMMIT")

    def migrate(self) -> list[str]:
        """Apply ``migrations/NNNN_*.sql`` in order, once each. Returns the names applied now."""
        conn = self.conn
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
        done = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}
        applied: list[str] = []
        for script in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if script.name in done:
                continue
            conn.executescript(script.read_text())
            conn.execute("INSERT INTO schema_migrations (name) VALUES (?)", (script.name,))
            applied.append(script.name)
        return applied

    def close(self) -> None:
        with self._lock:
            for conn in self._opened:
                conn.close()
            self._opened.clear()
        self._local = threading.local()
