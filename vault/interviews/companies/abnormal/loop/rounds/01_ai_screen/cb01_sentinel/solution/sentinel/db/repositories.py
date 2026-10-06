"""Event persistence. Every query takes a tenant_id; there is no unscoped read."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from sentinel.models import SecurityEvent
from sentinel.timeutil import iso, parse_ts


def _row_to_event(row: sqlite3.Row) -> SecurityEvent:
    return SecurityEvent(
        id=row["id"],
        tenant_id=row["tenant_id"],
        ts=parse_ts(row["ts"]),
        source=row["source"],
        kind=row["kind"],
        user=row["user"],
        src_ip=row["src_ip"],
        attrs=json.loads(row["attrs"]),
        enrichment=json.loads(row["enrichment"]),
    )


class EventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, event: SecurityEvent) -> None:
        """Insert or replace (re-ingesting the same file is idempotent)."""
        self.conn.execute(
            "INSERT OR REPLACE INTO events (tenant_id, id, ts, source, kind, user, src_ip, attrs, enrichment)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event.tenant_id,
                event.id,
                iso(event.ts),
                event.source,
                event.kind,
                event.user,
                event.src_ip,
                json.dumps(event.attrs, sort_keys=True),
                json.dumps(event.enrichment, sort_keys=True),
            ),
        )
        self.conn.commit()

    def get(self, tenant_id: str, event_id: str) -> SecurityEvent | None:
        row = self.conn.execute(
            "SELECT * FROM events WHERE tenant_id = ? AND id = ?", (tenant_id, event_id)
        ).fetchone()
        return _row_to_event(row) if row else None

    def history_for_user(
        self, tenant_id: str, user: str, before: datetime, limit: int = 500
    ) -> list[SecurityEvent]:
        """The user's most recent events strictly before ``before``, newest first."""
        rows = self.conn.execute(
            "SELECT * FROM events WHERE tenant_id = ? AND user = ? AND ts < ? ORDER BY ts DESC LIMIT ?",
            (tenant_id, user, iso(before), limit),
        ).fetchall()
        return [_row_to_event(r) for r in rows]

    def failed_logins_from_ip(
        self, tenant_id: str, src_ip: str, since: datetime, until: datetime
    ) -> list[datetime]:
        """Timestamps of failed logins from one source address in [since, until)."""
        rows = self.conn.execute(
            "SELECT ts FROM events WHERE tenant_id = ? AND src_ip = ? AND kind = 'login_failure'"
            " AND ts >= ? AND ts < ? ORDER BY ts",
            (tenant_id, src_ip, iso(since), iso(until)),
        ).fetchall()
        return [parse_ts(r["ts"]) for r in rows]

    def count(self, tenant_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) AS n FROM events WHERE tenant_id = ?", (tenant_id,)
        ).fetchone()
        return int(row["n"])
