"""Domain models shared by every stage of the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any

from sentinel.timeutil import iso


class ThreatLevel(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class SecurityEvent:
    """A normalised event from any collector. ``enrichment`` is filled in by the enrichment stage."""

    id: str
    tenant_id: str
    ts: datetime
    source: str
    kind: str
    user: str | None = None
    src_ip: str | None = None
    attrs: dict[str, Any] = field(default_factory=dict)
    enrichment: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "ts": iso(self.ts),
            "source": self.source,
            "kind": self.kind,
            "user": self.user,
            "src_ip": self.src_ip,
            "attrs": self.attrs,
            "enrichment": self.enrichment,
        }


@dataclass(frozen=True)
class RuleHit:
    """One detection fired by one rule for one event."""

    rule_id: str
    severity: ThreatLevel
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)
