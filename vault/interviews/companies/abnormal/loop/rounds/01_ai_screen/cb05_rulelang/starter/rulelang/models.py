"""Domain models: ``Event`` goes in, ``Signal`` comes out."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from rulelang.addresses import domain_of

EVENT_KINDS = ("email", "login", "mailbox_rule_created")


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def rank(self) -> int:
        return list(Severity).index(self)


@dataclass(frozen=True)
class Event:
    """One thing that happened in a tenant.

    ``actor`` is the sender of an email or the user of a login / mailbox-rule event.
    """

    id: str
    tenant_id: str
    kind: str
    ts: datetime
    actor: str
    recipients: tuple[str, ...] = ()
    subject: str = ""
    links: tuple[str, ...] = ()
    attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def actor_domain(self) -> str:
        return domain_of(self.actor)


@dataclass(frozen=True)
class Signal:
    """A detector's finding about one event."""

    detector: str
    event_id: str
    tenant_id: str
    severity: Severity
    summary: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "detector": self.detector,
            "severity": self.severity.value,
            "summary": self.summary,
            "evidence": self.evidence,
        }
