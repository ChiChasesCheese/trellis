"""sqlite repositories. Every method takes ``tenant_id`` and scopes its SQL by it."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from quarantine.models import Attachment, Disposition, Report, ReportStatus, Verdict
from quarantine.timeutil import iso, parse_iso

_COLUMNS = (
    "id, tenant_id, message_id, reporter, sender, display_name, subject, sent_at, received_at, "
    "links, attachments, verdicts, disposition, status"
)


def _verdicts_json(verdicts: list[Verdict]) -> str:
    return json.dumps([v.to_dict() for v in verdicts])


def _row_to_report(row: sqlite3.Row) -> Report:
    return Report(
        id=row["id"],
        tenant_id=row["tenant_id"],
        message_id=row["message_id"],
        reporter=row["reporter"],
        sender=row["sender"],
        display_name=row["display_name"],
        subject=row["subject"],
        sent_at=parse_iso(row["sent_at"]),
        received_at=parse_iso(row["received_at"]),
        links=json.loads(row["links"]),
        attachments=[Attachment(**a) for a in json.loads(row["attachments"])],
        verdicts=[
            Verdict(v["analyzer"], v["score"], tuple(v["reasons"])) for v in json.loads(row["verdicts"])
        ],
        disposition=Disposition(row["disposition"]) if row["disposition"] else None,
        status=ReportStatus(row["status"]) if row["status"] else None,
    )


class ReportRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, report: Report) -> None:
        self.conn.execute(
            f"INSERT INTO reports ({_COLUMNS}) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                report.id,
                report.tenant_id,
                report.message_id,
                report.reporter,
                report.sender,
                report.display_name,
                report.subject,
                report.sent_at.isoformat(timespec="seconds"),
                iso(report.received_at),
                json.dumps(report.links),
                json.dumps([a.to_dict() for a in report.attachments]),
                _verdicts_json(report.verdicts),
                report.disposition.value if report.disposition else None,
                report.status.value if report.status else None,
            ),
        )
        self.conn.commit()

    def get(self, tenant_id: str, report_id: str) -> Report | None:
        row = self.conn.execute(
            f"SELECT {_COLUMNS} FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
        return _row_to_report(row) if row else None

    def find_by_message(self, tenant_id: str, message_id: str) -> Report | None:
        row = self.conn.execute(
            f"SELECT {_COLUMNS} FROM reports WHERE tenant_id = ? AND message_id = ?",
            (tenant_id, message_id),
        ).fetchone()
        return _row_to_report(row) if row else None

    def list(self, tenant_id: str, limit: int = 50, offset: int = 0) -> list[Report]:
        rows = self.conn.execute(
            f"SELECT {_COLUMNS} FROM reports WHERE tenant_id = ? "
            "ORDER BY received_at DESC, id LIMIT ? OFFSET ?",
            (tenant_id, limit, offset),
        ).fetchall()
        return [_row_to_report(r) for r in rows]

    def count(self, tenant_id: str) -> int:
        return self.conn.execute(
            "SELECT COUNT(*) FROM reports WHERE tenant_id = ?", (tenant_id,)
        ).fetchone()[0]

    def update_outcome(
        self,
        tenant_id: str,
        report_id: str,
        verdicts: list[Verdict],
        disposition: Disposition,
        status: ReportStatus,
    ) -> None:
        self.conn.execute(
            "UPDATE reports SET verdicts = ?, disposition = ?, status = ? "
            "WHERE tenant_id = ? AND id = ?",
            (_verdicts_json(verdicts), disposition.value, status.value, tenant_id, report_id),
        )
        self.conn.commit()

    def set_status(self, tenant_id: str, report_id: str, status: ReportStatus) -> None:
        self.conn.execute(
            "UPDATE reports SET status = ? WHERE tenant_id = ? AND id = ?",
            (status.value, tenant_id, report_id),
        )
        self.conn.commit()

    def count_sender_reports(
        self, tenant_id: str, sender: str, since: datetime, until: datetime, exclude_message_id: str
    ) -> int:
        """Reports of other messages from ``sender`` whose Date header falls in [since, until]."""
        return self.conn.execute(
            "SELECT COUNT(*) FROM reports WHERE tenant_id = ? AND sender = ? "
            "AND message_id != ? AND sent_at >= ? AND sent_at <= ?",
            (
                tenant_id,
                sender,
                exclude_message_id,
                since.isoformat(timespec="seconds"),
                until.isoformat(timespec="seconds"),
            ),
        ).fetchone()[0]


class ActionLogRepository:
    """Append-only trail of everything done to a mailbox on a report's behalf."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def record(self, tenant_id: str, report_id: str, action: str, at: datetime, detail: str = "") -> None:
        self.conn.execute(
            "INSERT INTO action_log (tenant_id, report_id, action, detail, at) VALUES (?,?,?,?,?)",
            (tenant_id, report_id, action, detail, iso(at)),
        )
        self.conn.commit()

    def for_report(self, tenant_id: str, report_id: str) -> list[dict[str, str]]:
        rows = self.conn.execute(
            "SELECT action, detail, at FROM action_log WHERE tenant_id = ? AND report_id = ? ORDER BY id",
            (tenant_id, report_id),
        ).fetchall()
        return [dict(r) for r in rows]

    def count(self, tenant_id: str, report_id: str, action: str) -> int:
        return self.conn.execute(
            "SELECT COUNT(*) FROM action_log WHERE tenant_id = ? AND report_id = ? AND action = ?",
            (tenant_id, report_id, action),
        ).fetchone()[0]
