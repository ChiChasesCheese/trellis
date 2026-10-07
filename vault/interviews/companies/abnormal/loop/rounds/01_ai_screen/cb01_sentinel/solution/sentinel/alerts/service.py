from __future__ import annotations

import uuid
from collections.abc import Callable, Sequence
from datetime import datetime, timedelta

from sentinel import metrics, scoring
from sentinel.alerts import Alert
from sentinel.alerts.repository import AlertRepository
from sentinel.config import Settings
from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.timeutil import utcnow

MAX_EVENT_IDS = 100  # event_count keeps the true total; the id list is capped


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
        """Turn the hits on one event into an alert: merge into a recent OPEN alert for the same
        source, or open a new one."""
        rule_ids = sorted({h.rule_id for h in hits})
        key = dedup_key(rule_ids, event)
        window = timedelta(minutes=self.settings.alerts.dedup_window_minutes)
        existing = (
            self.repo.find_open(event.tenant_id, key, event.ts - window) if window else None
        )
        level = scoring.combine(hits, self.settings.threat.escalate_at)
        if existing is not None:
            return self._merge(existing, event, level)
        return self._open(event, hits, rule_ids, key, level)

    def _score(self, event: SecurityEvent, level: ThreatLevel, event_count: int) -> float:
        crit = self.assets.criticality(event.tenant_id, event.user, event.attrs.get("host"))
        age_hours = (self.clock() - event.ts).total_seconds() / 3600
        r = self.settings.ranking
        return scoring.score(level, r.weights, crit, age_hours, r.half_life_hours, event_count)

    def _open(self, event, hits, rule_ids, key, level) -> Alert:
        top = max(hits, key=lambda h: h.severity)
        alert = Alert(
            id=f"al_{uuid.uuid4().hex[:10]}",
            tenant_id=event.tenant_id,
            title=top.reason,
            rule_ids=rule_ids,
            threat_level=level,
            score=self._score(event, level, 1),
            created_at=event.ts,
            event_ids=[event.id],
            last_seen=event.ts,
            dedup_key=key,
        )
        self.repo.add(alert)
        metrics.incr("alerts.created", level=level.name)
        return alert

    def _merge(self, alert: Alert, event: SecurityEvent, level: ThreatLevel) -> Alert:
        alert.event_count += 1
        alert.event_ids = [*alert.event_ids, event.id][-MAX_EVENT_IDS:]
        alert.last_seen = max(alert.last_seen or event.ts, event.ts)
        alert.threat_level = max(alert.threat_level, level)
        alert.score = self._score(event, alert.threat_level, alert.event_count)
        self.repo.update_activity(alert)
        metrics.incr("alerts.merged", level=alert.threat_level.name)
        return alert


def dedup_key(rule_ids: Sequence[str], event: SecurityEvent) -> str:
    """Two events fold into one alert when they trip the same rules for the same user and source address."""
    return "|".join([",".join(rule_ids), event.user or "", event.src_ip or ""])
