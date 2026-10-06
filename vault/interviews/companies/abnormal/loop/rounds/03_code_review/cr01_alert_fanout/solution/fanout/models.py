"""Domain models shared by the digest job and the fan-out worker."""
from __future__ import annotations

import json
from dataclasses import dataclass


class MalformedAlert(ValueError):
    """The message body is not a valid alert."""


@dataclass(frozen=True)
class Alert:
    tenant_id: str
    alert_id: str
    rule: str
    severity: int  # 1 (info) .. 5 (critical)
    title: str
    user: str
    created_at: str  # ISO-8601 UTC, e.g. 2026-10-01T12:00:00Z

    @classmethod
    def from_json(cls, body: str) -> "Alert":
        try:
            raw = json.loads(body)
            return cls(
                tenant_id=str(raw["tenant_id"]),
                alert_id=str(raw["alert_id"]),
                rule=str(raw["rule"]),
                severity=int(raw["severity"]),
                title=str(raw["title"]),
                user=str(raw.get("user", "")),
                created_at=str(raw["created_at"]),
            )
        except (ValueError, KeyError, TypeError) as exc:
            raise MalformedAlert(f"bad alert payload: {exc}") from exc

    @property
    def dedup_key(self) -> str:
        """Stable identity of an alert. Alert ids are only unique within a tenant."""
        return f"{self.tenant_id}:{self.rule}:{self.alert_id}"


@dataclass(frozen=True)
class Channel:
    tenant_id: str
    kind: str  # "webhook" | "email" | "slack"
    target: str  # URL, address or channel name
    secret: str = ""
    min_severity: int = 1
