"""Cases: one analyst-facing item per incident instead of one per alert.

An alert joins the user's open case when it arrives within `case_window_hours` of that case's
latest alert; otherwise it opens a new case. Closed cases are never reopened. A case's score is
the highest score among its alerts (one 0.9 alert is worse than ten 0.2 ones).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from ..config import Config
from ..errors import InsiderWatchError
from ..scoring import severity_label
from ..timeutil import parse_ts
from .models import Alert

_SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2}


@dataclass
class Case:
    id: int
    user: str
    status: str
    score: float
    opened_at: datetime
    last_alert_at: datetime
    closed_at: datetime | None = None
    alert_ids: list[int] = field(default_factory=list)

    def to_dict(self, config: Config) -> dict[str, Any]:
        return {
            "id": self.id,
            "user": self.user,
            "status": self.status,
            "severity": severity_label(self.score, config),
            "score": self.score,
            "opened_at": self.opened_at.isoformat(),
            "last_alert_at": self.last_alert_at.isoformat(),
            "alerts": self.alert_ids,
        }


@dataclass(frozen=True)
class CaseChange:
    case: Case
    created: bool
    escalated: bool


class CaseStore:
    def __init__(self, conn: sqlite3.Connection, config: Config) -> None:
        self._conn = conn
        self._config = config

    def _hydrate(self, row: sqlite3.Row) -> Case:
        ids = self._conn.execute("SELECT alert_id FROM case_alerts WHERE case_id = ? ORDER BY alert_id", (row["id"],))
        return Case(
            id=row["id"], user=row["user"], status=row["status"], score=row["score"],
            opened_at=parse_ts(row["opened_at"]), last_alert_at=parse_ts(row["last_alert_at"]),
            closed_at=parse_ts(row["closed_at"]) if row["closed_at"] else None,
            alert_ids=[r["alert_id"] for r in ids],
        )

    def assign(self, alert: Alert) -> CaseChange:
        """File `alert` (already stored, has an id) into a case."""
        window = timedelta(hours=self._config.case_window_hours)
        row = self._conn.execute(
            "SELECT * FROM cases WHERE user = ? AND status = 'open' AND last_alert_at >= ? "
            "ORDER BY last_alert_at DESC LIMIT 1", (alert.user, (alert.ts - window).isoformat())).fetchone()
        with self._conn:
            if row is None:
                cur = self._conn.execute(
                    "INSERT INTO cases (user, score, opened_at, last_alert_at) VALUES (?,?,?,?)",
                    (alert.user, alert.score, alert.ts.isoformat(), alert.ts.isoformat()))
                case_id, created, escalated = cur.lastrowid, True, False
            else:
                case_id, created = row["id"], False
                old, new = severity_label(row["score"], self._config), severity_label(max(row["score"], alert.score), self._config)
                escalated = _SEVERITY_ORDER[new] > _SEVERITY_ORDER[old]
                self._conn.execute(
                    "UPDATE cases SET score = MAX(score, ?), last_alert_at = MAX(last_alert_at, ?) WHERE id = ?",
                    (alert.score, alert.ts.isoformat(), case_id))
            self._conn.execute("INSERT INTO case_alerts (alert_id, case_id) VALUES (?, ?)", (alert.id, case_id))
        return CaseChange(self.get(case_id), created, escalated)

    def get(self, case_id: int) -> Case | None:
        row = self._conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
        return self._hydrate(row) if row else None

    def list(self, user: str | None = None) -> list[Case]:
        sql, args = "SELECT * FROM cases", ()
        if user:
            sql, args = sql + " WHERE user = ?", (user.strip().lower(),)
        return [self._hydrate(r) for r in self._conn.execute(sql + " ORDER BY opened_at, id", args)]

    def close(self, case_id: int) -> Case:
        case = self.get(case_id)
        if case is None:
            raise InsiderWatchError(f"no such case: {case_id}")
        if case.status == "closed":
            raise InsiderWatchError(f"case {case_id} is already closed")
        with self._conn:
            self._conn.execute("UPDATE cases SET status = 'closed', closed_at = ? WHERE id = ?",
                               (datetime.now(timezone.utc).isoformat(), case_id))
        return self.get(case_id)
