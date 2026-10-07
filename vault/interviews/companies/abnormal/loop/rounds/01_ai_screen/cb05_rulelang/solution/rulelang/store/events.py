"""Event persistence. Every query takes ``tenant_id``."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from rulelang.models import Event
from rulelang.timeutil import iso, parse_ts


def _row_to_event(row: sqlite3.Row) -> Event:
    payload = json.loads(row["payload"])
    return Event(
        id=row["id"],
        tenant_id=row["tenant_id"],
        kind=row["kind"],
        ts=parse_ts(row["ts"]),
        actor=row["actor"],
        recipients=tuple(payload["recipients"]),
        subject=payload["subject"],
        links=tuple(payload["links"]),
        attrs=payload["attrs"],
    )


class EventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, event: Event) -> None:
        payload = {
            "recipients": list(event.recipients),
            "subject": event.subject,
            "links": list(event.links),
            "attrs": event.attrs,
        }
        self.conn.execute(
            "INSERT OR REPLACE INTO events (tenant_id, id, kind, ts, actor, payload) VALUES (?,?,?,?,?,?)",
            (event.tenant_id, event.id, event.kind, iso(event.ts), event.actor, json.dumps(payload)),
        )
        self.conn.commit()

    def get(self, tenant_id: str, event_id: str) -> Event | None:
        row = self.conn.execute(
            "SELECT * FROM events WHERE tenant_id = ? AND id = ?", (tenant_id, event_id)
        ).fetchone()
        return _row_to_event(row) if row else None

    def last_login(self, tenant_id: str, user: str, before: datetime) -> Event | None:
        """The user's most recent login strictly before ``before``."""
        row = self.conn.execute(
            "SELECT * FROM events WHERE tenant_id = ? AND kind = 'login' AND actor = ? AND ts < ?"
            " ORDER BY ts DESC, id DESC LIMIT 1",
            (tenant_id, user, iso(before)),
        ).fetchone()
        return _row_to_event(row) if row else None

    def count_emails_from(self, tenant_id: str, sender: str, since: datetime, until: datetime) -> int:
        """Emails ``sender`` sent in ``[since, until)``."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM events WHERE tenant_id = ? AND kind = 'email' AND actor = ?"
            " AND ts >= ? AND ts < ?",
            (tenant_id, sender, iso(since), iso(until)),
        ).fetchone()
        return int(row[0])
