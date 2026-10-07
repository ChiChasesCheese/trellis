"""SQLite access and schema migrations.

Schema changes are new numbered files in `insiderwatch/migrations/`; applied files are never edited.
"""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
log = logging.getLogger(__name__)


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Apply pending migrations in filename order; returns the names applied."""
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
    done = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}
    applied: list[str] = []
    for sql_file in sorted(MIGRATIONS_DIR.glob("[0-9]*.sql")):
        if sql_file.name in done:
            continue
        conn.executescript(sql_file.read_text())
        conn.execute("INSERT INTO schema_migrations (name) VALUES (?)", (sql_file.name,))
        conn.commit()
        applied.append(sql_file.name)
        log.info("applied migration %s", sql_file.name)
    return applied


def open_db(path: str | Path) -> sqlite3.Connection:
    conn = connect(path)
    migrate(conn)
    return conn
