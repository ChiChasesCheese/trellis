"""SQLite storage. ``connect`` applies pending migrations; ``Store`` bundles the repositories."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from vetting.store.repositories import (
    IdentityRepository,
    ObservationRepository,
    ReviewRepository,
)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Apply ``migrations/NNNN_*.sql`` in order, once each. Returns the versions applied now."""
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY)")
    done = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}
    applied = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if path.stem in done:
            continue
        conn.executescript(path.read_text())
        conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (path.stem,))
        applied.append(path.stem)
    conn.commit()
    return applied


def connect(path: str | Path) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    migrate(conn)
    return conn


class Store:
    """Repositories over one connection. Every query takes the tenant id first."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.identities = IdentityRepository(conn)
        self.observations = ObservationRepository(conn)
        self.reviews = ReviewRepository(conn)

    @classmethod
    def open(cls, path: str | Path) -> "Store":
        return cls(connect(path))

    def close(self) -> None:
        self.conn.close()
