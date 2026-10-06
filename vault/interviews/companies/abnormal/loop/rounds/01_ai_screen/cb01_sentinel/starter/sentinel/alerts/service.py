from __future__ import annotations

import uuid
from collections.abc import Callable, Sequence
from datetime import datetime

from sentinel import metrics, scoring
from sentinel.alerts import Alert
from sentinel.alerts.repository import AlertRepository
from sentinel.config import Settings
from sentinel.models import RuleHit, SecurityEvent
from sentinel.timeutil import utcnow


class AlertService:
    def __init__(
        self,
        settings: Settings,
        repo: AlertRepository,
        assets: scoring.AssetCatalog,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.settings = settings
        self.repo = repo
        self.assets = assets
        self.clock = clock

    def create_from(self, event: SecurityEvent, hits: Sequence[RuleHit]) -> Alert:
        """Turn the hits on one event into a stored, scored alert."""
        level = scoring.combine(hits, self.settings.threat.escalate_at)
        crit = self.assets.criticality(event.tenant_id, event.user, event.attrs.get("host"))
        age_hours = (self.clock() - event.ts).total_seconds() / 3600
        top = max(hits, key=lambda h: h.severity)
        alert = Alert(
            id=f"al_{uuid.uuid4().hex[:10]}",
            tenant_id=event.tenant_id,
            title=top.reason,
            rule_ids=sorted({h.rule_id for h in hits}),
            threat_level=level,
            score=scoring.score(
                level,
                self.settings.ranking.weights,
                crit,
                age_hours,
                self.settings.ranking.half_life_hours,
            ),
            created_at=event.ts,
            event_ids=[event.id],
        )
        self.repo.add(alert)
        metrics.incr("alerts.created", level=level.name)
        return alert
