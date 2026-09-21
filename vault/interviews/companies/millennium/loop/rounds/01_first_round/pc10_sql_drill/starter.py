"""pc10 SQL Drill -- candidate starter.

Fill in part1..part5, each returning a SQL string, to run against the sqlite3 database defined by
schema.sql + seed.sql in this directory (three tables: trades / instruments / fx_rates). See
problem.md for the full schema, rules and worked examples.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


def part1() -> str:
    return ""


def part2() -> str:
    return ""


def part3() -> str:
    return ""


def part4() -> str:
    return ""


def part5() -> str:
    return ""


def _connect() -> sqlite3.Connection:
    base = Path(__file__).resolve().parent
    conn = sqlite3.connect(":memory:")
    conn.executescript((base / "schema.sql").read_text())
    conn.executescript((base / "seed.sql").read_text())
    return conn


def _format_row(row: tuple) -> str:
    return "\t".join("" if v is None else str(v) for v in row)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    sql = {1: part1, 2: part2, 3: part3, 4: part4, 5: part5}[n]()
    conn = _connect()
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    out = [_format_row(row) for row in rows]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
