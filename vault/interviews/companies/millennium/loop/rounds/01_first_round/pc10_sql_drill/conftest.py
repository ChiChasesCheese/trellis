"""pc10-local fixture: a fresh in-memory sqlite3 database, seeded from schema.sql + seed.sql in
this directory, for each test. `impl`/`run_script` come from the shared root conftest.py."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.executescript((_HERE / "schema.sql").read_text())
    conn.executescript((_HERE / "seed.sql").read_text())
    try:
        yield conn
    finally:
        conn.close()
