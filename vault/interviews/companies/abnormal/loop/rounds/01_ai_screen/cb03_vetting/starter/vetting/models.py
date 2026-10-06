"""Domain model shared by sources, signals, scoring, storage and the API."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any

from vetting.timeutil import parse_ts, to_iso


class Kind(StrEnum):
    """What an observation is a value of."""

    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    COUNTRY = "country"  # country the applicant says they are in
    IP = "ip"  # IP the application was submitted from
    USER_AGENT = "user_agent"
    RESUME_SHA256 = "resume_sha256"
    RESUME_AUTHOR = "resume_author"
    RESUME_TOOL = "resume_tool"
    RESUME_NAME = "resume_name"
    RESUME_EMAIL = "resume_email"
    RESUME_PHONE = "resume_phone"
    LOGIN_IP = "login_ip"  # identity-provider sign-in before the start date
    LOGIN_COUNTRY = "login_country"
    DEVICE = "device"


class Recommendation(StrEnum):
    HIGHLY_RECOMMENDED = "HIGHLY_RECOMMENDED"
    RECOMMENDED = "RECOMMENDED"
    NONE = "NONE"

    @property
    def rank(self) -> int:
        return {"NONE": 0, "RECOMMENDED": 1, "HIGHLY_RECOMMENDED": 2}[self.value]


DECISIONS = ("cleared", "escalated")


@dataclass(frozen=True)
class Identity:
    """One applicant at one customer organization (tenant)."""

    id: str
    tenant_id: str
    source: str
    external_id: str
    display_name: str
    applied_at: datetime

    @staticmethod
    def make_id(source: str, external_id: str) -> str:
        return f"{source}:{external_id}"


@dataclass(frozen=True)
class Observation:
    """A single value seen for an identity. ``value`` is as submitted; ``raw_ref`` is
    ``<identity_id>#<path into the source record>`` and is what citations point at."""

    identity_id: str
    tenant_id: str
    kind: Kind
    value: str
    source: str
    ts: datetime
    raw_ref: str


@dataclass(frozen=True)
class Citation:
    source: str
    ref: str
    ts: datetime

    @classmethod
    def of(cls, obs: Observation) -> "Citation":
        return cls(source=obs.source, ref=obs.raw_ref, ts=obs.ts)

    def to_dict(self) -> dict[str, str]:
        return {"source": self.source, "ref": self.ref, "ts": to_iso(self.ts)}


@dataclass(frozen=True)
class Finding:
    """Something a signal found. ``subject`` names the specific value it fired on (for example
    ``asn:AS64500`` or ``phone:+14155550100``); it is empty when no single value is to blame."""

    signal: str
    weight: int
    summary: str
    evidence: tuple[Citation, ...] = ()
    subject: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal": self.signal,
            "weight": self.weight,
            "summary": self.summary,
            "subject": self.subject,
            "evidence": [c.to_dict() for c in self.evidence],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Finding":
        return cls(
            signal=data["signal"],
            weight=int(data["weight"]),
            summary=data["summary"],
            subject=data.get("subject", ""),
            evidence=tuple(
                Citation(c["source"], c["ref"], parse_ts(c["ts"])) for c in data.get("evidence", [])
            ),
        )


@dataclass
class Review:
    tenant_id: str
    identity_id: str
    recommendation: Recommendation
    score: int
    findings: list[Finding] = field(default_factory=list)
    evaluated_at: datetime | None = None


@dataclass(frozen=True)
class Disposition:
    identity_id: str
    decision: str
    note: str
    decided_at: datetime
