"""sqlite access shared by the API and the nightly scoring job."""
from __future__ import annotations

import hashlib
import sqlite3
import threading
from typing import Sequence

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    tenant_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL DEFAULT '',
    risk_score INTEGER NOT NULL DEFAULT 0,   -- denormalised by the nightly job
    PRIMARY KEY (tenant_id, user_id)
);
CREATE TABLE IF NOT EXISTS signals (
    tenant_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    weight INTEGER NOT NULL,
    observed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS signals_user ON signals (tenant_id, user_id);
CREATE TABLE IF NOT EXISTS api_keys (
    key_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    key_hash TEXT NOT NULL
);
"""


class Database:
    def __init__(self, path: str = ":memory:"):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.executescript(SCHEMA)

    def query(self, sql: str, params: Sequence = ()) -> list[tuple]:
        with self._lock:
            return self._conn.execute(sql, params).fetchall()

    def execute(self, sql: str, params: Sequence = ()) -> None:
        with self._lock:
            self._conn.execute(sql, params)
            self._conn.commit()


def hash_secret(secret: str) -> str:
    """API secrets are long random strings, so a plain SHA-256 digest is enough (no password KDF needed)."""
    return hashlib.sha256(secret.encode()).hexdigest()


def create_api_key(db: Database, tenant_id: str, key_id: str, secret: str) -> None:
    """Register an API key. Clients send `<key_id>.<secret>`; only a digest of the secret is stored."""
    db.execute(
        "INSERT INTO api_keys (key_id, tenant_id, key_hash) VALUES (?, ?, ?)",
        (key_id, tenant_id, hash_secret(secret)),
    )


def add_user(db: Database, tenant_id: str, user_id: str, email: str, name: str, department: str = "", risk_score: int = 0) -> None:
    db.execute(
        "INSERT INTO users (tenant_id, user_id, email, name, department, risk_score) VALUES (?,?,?,?,?,?)",
        (tenant_id, user_id, email, name, department, risk_score),
    )


def add_signal(db: Database, tenant_id: str, user_id: str, kind: str, weight: int, observed_at: str) -> None:
    db.execute(
        "INSERT INTO signals (tenant_id, user_id, kind, weight, observed_at) VALUES (?,?,?,?,?)",
        (tenant_id, user_id, kind, weight, observed_at),
    )
