"""Alerts: the ``Alert`` model, its repository and the service that creates them."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from sentinel.models import ThreatLevel
from sentinel.timeutil import iso


class AlertStatus(str, Enum):
    OPEN = "OPEN"
    ACKED = "ACKED"
    CLOSED = "CLOSED"


@dataclass
class Alert:
    id: str
    tenant_id: str
    title: str
    rule_ids: list[str]
    threat_level: ThreatLevel
    score: float
    created_at: datetime
    event_ids: list[str] = field(default_factory=list)
    status: AlertStatus = AlertStatus.OPEN
    event_count: int = 1
    last_seen: datetime | None = None
    dedup_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "rule_ids": self.rule_ids,
            "threat_level": self.threat_level.name,
            "score": self.score,
            "status": self.status.value,
            "created_at": iso(self.created_at),
            "event_ids": self.event_ids,
            "event_count": self.event_count,
            "last_seen": iso(self.last_seen or self.created_at),
        }


from sentinel.alerts.repository import AlertRepository  # noqa: E402
from sentinel.alerts.service import AlertService  # noqa: E402

__all__ = ["Alert", "AlertRepository", "AlertService", "AlertStatus"]
