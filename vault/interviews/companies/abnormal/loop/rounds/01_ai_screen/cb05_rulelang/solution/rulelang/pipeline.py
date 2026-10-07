"""load -> detect -> store signals -> update the communication graph."""
from __future__ import annotations

import logging
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from rulelang import metrics
from rulelang.config import Settings, SettingsProvider
from rulelang.detectors import DetectorRunner
from rulelang.events import load_events
from rulelang.graph import CommGraph
from rulelang.models import Event, Signal
from rulelang.store import EventRepository, SignalRepository

log = logging.getLogger(__name__)


@dataclass
class _TenantRuntime:
    settings: Settings
    graph: CommGraph
    runner: DetectorRunner


class Pipeline:
    def __init__(self, conn: sqlite3.Connection, settings: SettingsProvider):
        self.conn = conn
        self.settings = settings
        self.events = EventRepository(conn)
        self.signals = SignalRepository(conn)
        self._runtimes: dict[str, _TenantRuntime] = {}

    def _runtime(self, tenant_id: str) -> _TenantRuntime:
        if tenant_id not in self._runtimes:
            settings = self.settings.for_tenant(tenant_id)
            graph = CommGraph(self.conn, tenant_id)
            self._runtimes[tenant_id] = _TenantRuntime(
                settings=settings,
                graph=graph,
                runner=DetectorRunner(settings, graph, self.events),
            )
        return self._runtimes[tenant_id]

    def ingest_dir(self, root: Path, tenant_id: str) -> list[Signal]:
        """Load every ``*.jsonl`` under ``root`` for one tenant and run the pipeline."""
        self.settings.for_tenant(tenant_id)  # fail fast on an unknown/invalid tenant config
        return self.run(load_events(root, tenant_id))

    def run(self, events: Iterable[Event]) -> list[Signal]:
        """Process events oldest-first; returns every signal they produced."""
        out: list[Signal] = []
        for event in sorted(events, key=lambda e: (e.ts, e.id)):
            out.extend(self.process(event))
        return out

    def process(self, event: Event) -> list[Signal]:
        runtime = self._runtime(event.tenant_id)
        signals = runtime.runner.run(event)
        # Stored after detection so "first contact" and "previous login" only see *earlier* events.
        self.events.add(event)
        runtime.graph.record(event)
        self.signals.add_many(signals)
        metrics.incr("pipeline.events")
        return signals
