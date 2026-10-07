from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from ..timeutil import parse_ts
from .models import Alert


def _row_to_alert(row: sqlite3.Row) -> Alert:
    return Alert(
        id=row["id"],
        user=row["user"],
        signal=row["signal"],
        score=row["score"],
        ts=parse_ts(row["ts"]),
        reasons=json.loads(row["reasons"]),
        evidence=json.loads(row["evidence"]),
    )


class AlertStore:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def add(self, alert: Alert) -> Alert:
        with self._conn:
            cur = self._conn.execute(
                "INSERT INTO alerts (user, signal, score, ts, reasons, evidence, created_at) VALUES (?,?,?,?,?,?,?)",
                (alert.user, alert.signal, alert.score, alert.ts.isoformat(), json.dumps(alert.reasons),
                 json.dumps(alert.evidence, default=str), datetime.now(timezone.utc).isoformat()),
            )
        alert.id = cur.lastrowid
        return alert

    def get(self, alert_id: int) -> Alert | None:
        row = self._conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
        return _row_to_alert(row) if row else None

    def list(self, user: str | None = None) -> list[Alert]:
        sql, args = "SELECT * FROM alerts", ()
        if user:
            sql, args = sql + " WHERE user = ?", (user.strip().lower(),)
        rows = self._conn.execute(sql + " ORDER BY ts, id", args).fetchall()
        return [_row_to_alert(r) for r in rows]
