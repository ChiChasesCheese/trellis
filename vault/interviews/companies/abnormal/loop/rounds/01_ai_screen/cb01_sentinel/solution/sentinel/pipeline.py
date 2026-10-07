"""collect -> enrich -> rules -> threat -> alert -> store."""
from __future__ import annotations

import logging
import sqlite3
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sentinel import metrics
from sentinel.alerts import Alert, AlertRepository, AlertService
from sentinel.collectors import collect_all
from sentinel.config import Settings, SettingsProvider
from sentinel.db import EventRepository
from sentinel.enrichment import EnrichmentService
from sentinel.models import SecurityEvent
from sentinel.scoring import AssetCatalog
from sentinel.suppressions import SuppressionRepository, SuppressionService
from sentinel.rules import RuleContext, RuleEngine
from sentinel.timeutil import utcnow

log = logging.getLogger(__name__)


@dataclass
class _TenantRuntime:
    settings: Settings
    enrichment: EnrichmentService
    rules: RuleEngine
    alerts: AlertService
    suppressions: SuppressionService


class Pipeline:
    def __init__(
        self,
        conn: sqlite3.Connection,
        settings: SettingsProvider,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.conn = conn
        self.settings = settings
        self.clock = clock
        self.events = EventRepository(conn)
        self._runtimes: dict[str, _TenantRuntime] = {}

    def _runtime(self, tenant_id: str) -> _TenantRuntime:
        if tenant_id not in self._runtimes:
            settings = self.settings.for_tenant(tenant_id)
            self._runtimes[tenant_id] = _TenantRuntime(
                settings=settings,
                enrichment=EnrichmentService(settings, self.events),
                rules=RuleEngine(settings),
                alerts=AlertService(
                    settings,
                    AlertRepository(self.conn),
                    AssetCatalog(settings.alerts.assets),
                    self.clock,
                ),
                suppressions=SuppressionService(SuppressionRepository(self.conn), self.clock),
            )
        return self._runtimes[tenant_id]

    def ingest_dir(self, root: Path, tenant_id: str) -> list[Alert]:
        """Collect every source under ``root`` for one tenant and run the pipeline."""
        self._runtime(tenant_id)  # fail fast on a bad tenant config (unknown enrichers, broken plugin)
        return self.run(collect_all(root, tenant_id))

    def run(self, events: Iterable[SecurityEvent]) -> list[Alert]:
        """Process events oldest-first; returns the alerts they created or updated (each once)."""
        touched: dict[str, Alert] = {}
        for event in sorted(events, key=lambda e: (e.ts, e.id)):
            alert = self.process(event)
            if alert is not None:
                touched[alert.id] = alert
        return list(touched.values())

    def process(self, event: SecurityEvent) -> Alert | None:
        runtime = self._runtime(event.tenant_id)
        runtime.enrichment.enrich(event)
        hits = runtime.rules.evaluate(event, RuleContext(events=self.events))
        hits = runtime.suppressions.apply(event, hits)
        # Stored after evaluation so history and brute-force counts only see *earlier* events.
        self.events.add(event)
        metrics.incr("pipeline.events")
        if not hits:
            return None
        return runtime.alerts.create_from(event, hits)
