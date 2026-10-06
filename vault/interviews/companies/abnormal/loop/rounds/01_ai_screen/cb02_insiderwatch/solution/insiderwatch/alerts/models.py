from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Alert:
    user: str
    signal: str
    score: float
    ts: datetime
    reasons: list[str]
    evidence: dict[str, Any] = field(default_factory=dict)
    id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user": self.user,
            "signal": self.signal,
            "score": self.score,
            "ts": self.ts.isoformat(),
            "reasons": self.reasons,
            "evidence": self.evidence,
        }
