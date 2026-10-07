"""Domain dataclasses: Report, Verdict, Attachment and the two enums."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Disposition(str, Enum):
    """What the decision step recommends for a reported message."""

    QUARANTINE = "QUARANTINE"
    RELEASE = "RELEASE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class ReportStatus(str, Enum):
    """Where the message is now."""

    QUARANTINED = "QUARANTINED"      # pulled from mailboxes
    NEEDS_REVIEW = "NEEDS_REVIEW"    # left in place, waiting for a human
    CLEARED = "CLEARED"              # analysed, nothing found, left in place
    RELEASED = "RELEASED"            # an admin put it back


def status_for(disposition: Disposition) -> ReportStatus:
    return {
        Disposition.QUARANTINE: ReportStatus.QUARANTINED,
        Disposition.NEEDS_REVIEW: ReportStatus.NEEDS_REVIEW,
        Disposition.RELEASE: ReportStatus.CLEARED,
    }[disposition]


@dataclass(frozen=True)
class Attachment:
    filename: str
    content_type: str = "application/octet-stream"
    size: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"filename": self.filename, "content_type": self.content_type, "size": self.size}


@dataclass(frozen=True)
class Verdict:
    """One analyzer's opinion: a 0-100 risk score and the reasons behind it."""

    analyzer: str
    score: int
    reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {"analyzer": self.analyzer, "score": self.score, "reasons": list(self.reasons)}


@dataclass
class Report:
    id: str
    tenant_id: str
    message_id: str
    reporter: str
    sender: str
    display_name: str
    subject: str
    sent_at: datetime
    received_at: datetime
    links: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    verdicts: list[Verdict] = field(default_factory=list)
    disposition: Disposition | None = None
    status: ReportStatus | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "message_id": self.message_id,
            "reporter": self.reporter,
            "sender": self.sender,
            "subject": self.subject,
            "sent_at": self.sent_at.isoformat(timespec="seconds"),
            "received_at": self.received_at.isoformat(timespec="seconds"),
            "links": list(self.links),
            "attachments": [a.to_dict() for a in self.attachments],
            "verdicts": [v.to_dict() for v in self.verdicts],
            "disposition": self.disposition.value if self.disposition else None,
            "status": self.status.value if self.status else None,
        }
