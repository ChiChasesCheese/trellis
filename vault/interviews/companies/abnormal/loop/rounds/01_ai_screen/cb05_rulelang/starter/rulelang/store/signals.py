"""Signal persistence. One row per (tenant, event, detector); re-running an event replaces it."""
from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable

from rulelang.models import Severity, Signal


def _row_to_signal(row: sqlite3.Row) -> Signal:
    return Signal(
        detector=row["detector"],
        event_id=row["event_id"],
        tenant_id=row["tenant_id"],
        severity=Severity(row["severity"]),
        summary=row["summary"],
        evidence=json.loads(row["evidence"]),
    )


class SignalRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_many(self, signals: Iterable[Signal]) -> None:
        self.conn.executemany(
            "INSERT OR REPLACE INTO signals (tenant_id, event_id, detector, severity, summary, evidence)"
            " VALUES (?,?,?,?,?,?)",
            [
                (s.tenant_id, s.event_id, s.detector, s.severity.value, s.summary, json.dumps(s.evidence))
                for s in signals
            ],
        )
        self.conn.commit()

    def for_event(self, tenant_id: str, event_id: str) -> list[Signal]:
        rows = self.conn.execute(
            "SELECT * FROM signals WHERE tenant_id = ? AND event_id = ? ORDER BY detector",
            (tenant_id, event_id),
        ).fetchall()
        return [_row_to_signal(r) for r in rows]

    def list(self, tenant_id: str, limit: int = 50) -> list[Signal]:
        rows = self.conn.execute(
            "SELECT * FROM signals WHERE tenant_id = ? ORDER BY event_id, detector LIMIT ?",
            (tenant_id, limit),
        ).fetchall()
        return [_row_to_signal(r) for r in rows]
