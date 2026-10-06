"""Alert persistence (sqlite). Every method is scoped by tenant_id."""
from __future__ import annotations

import json
import sqlite3

from sentinel.alerts import Alert, AlertStatus
from sentinel.models import ThreatLevel
from sentinel.timeutil import iso, parse_ts


def _row_to_alert(row: sqlite3.Row) -> Alert:
    return Alert(
        id=row["id"],
        tenant_id=row["tenant_id"],
        title=row["title"],
        rule_ids=json.loads(row["rule_ids"]),
        threat_level=ThreatLevel(row["threat_level"]),
        score=row["score"],
        status=AlertStatus(row["status"]),
        created_at=parse_ts(row["created_at"]),
        event_ids=json.loads(row["event_ids"]),
    )


class AlertRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, alert: Alert) -> None:
        self.conn.execute(
            "INSERT INTO alerts (id, tenant_id, title, rule_ids, threat_level, score, status, created_at, event_ids)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                alert.id,
                alert.tenant_id,
                alert.title,
                json.dumps(alert.rule_ids),
                int(alert.threat_level),
                alert.score,
                alert.status.value,
                iso(alert.created_at),
                json.dumps(alert.event_ids),
            ),
        )
        self.conn.commit()

    def get(self, tenant_id: str, alert_id: str) -> Alert | None:
        row = self.conn.execute(
            "SELECT * FROM alerts WHERE tenant_id = ? AND id = ?", (tenant_id, alert_id)
        ).fetchone()
        return _row_to_alert(row) if row else None

    def list(
        self, tenant_id: str, status: AlertStatus | None = None, limit: int = 50, offset: int = 0
    ) -> list[Alert]:
        sql = "SELECT * FROM alerts WHERE tenant_id = ?"
        args: list = [tenant_id]
        if status is not None:
            sql += " AND status = ?"
            args.append(status.value)
        sql += " ORDER BY score DESC, created_at DESC, id LIMIT ? OFFSET ?"
        args += [limit, offset]
        return [_row_to_alert(r) for r in self.conn.execute(sql, args)]

    def count(self, tenant_id: str, status: AlertStatus | None = None) -> int:
        sql = "SELECT COUNT(*) AS n FROM alerts WHERE tenant_id = ?"
        args: list = [tenant_id]
        if status is not None:
            sql += " AND status = ?"
            args.append(status.value)
        return int(self.conn.execute(sql, args).fetchone()["n"])

    def set_status(self, tenant_id: str, alert_id: str, status: AlertStatus) -> bool:
        cur = self.conn.execute(
            "UPDATE alerts SET status = ? WHERE tenant_id = ? AND id = ?",
            (status.value, tenant_id, alert_id),
        )
        self.conn.commit()
        return cur.rowcount > 0
