"""Runs the tenant's enrichers for one event, in dependency order."""
from __future__ import annotations

import logging

from sentinel import metrics
from sentinel.config import Settings
from sentinel.db import EventRepository
from sentinel.enrichment.base import ENRICHERS, Enricher, EnrichmentContext
from sentinel.enrichment.plugins import discover
from sentinel.errors import ConfigError
from sentinel.models import SecurityEvent

log = logging.getLogger(__name__)


def resolve_order(names: list[str], available: dict[str, type[Enricher]]) -> list[type[Enricher]]:
    """Topologically sort ``names`` by ``requires`` (stable: ties keep the configured order)."""
    unknown = [n for n in names if n not in available]
    if unknown:
        raise ConfigError(
            f"unknown enrichers: {', '.join(sorted(unknown))} (available: {', '.join(sorted(available))})"
        )
    ordered: list[type[Enricher]] = []
    state: dict[str, str] = {}

    def visit(name: str, chain: tuple[str, ...]) -> None:
        if state.get(name) == "done":
            return
        if state.get(name) == "visiting":
            raise ConfigError(f"enrichers form a dependency cycle: {' -> '.join(chain + (name,))}")
        state[name] = "visiting"
        for dep in available[name].requires:
            if dep not in names:
                raise ConfigError(f"enricher {name!r} requires {dep!r}, which is not enabled")
            visit(dep, chain + (name,))
        state[name] = "done"
        ordered.append(available[name])

    for name in names:
        visit(name, ())
    return ordered


class EnrichmentService:
    def __init__(self, settings: Settings, events: EventRepository):
        self.settings = settings
        self._ctx = EnrichmentContext(settings=settings, events=events)
        cfg = settings.enrichment
        available = {**ENRICHERS, **discover(cfg.plugin_dirs)}
        names = list(cfg.enabled) if cfg.enabled is not None else sorted(ENRICHERS)
        self._enrichers = [cls(settings) for cls in resolve_order(names, available)]

    def enrich(self, event: SecurityEvent) -> SecurityEvent:
        """Mutates and returns ``event``. A failing enricher is logged and counted, never fatal."""
        for enricher in self._enrichers:
            if any(dep not in event.enrichment for dep in enricher.requires):
                metrics.incr("enrichment.skipped", enricher=enricher.name)
                continue
            try:
                event.enrichment[enricher.name] = enricher.enrich(event, self._ctx)
            except Exception:
                log.exception("enricher %s failed on event %s", enricher.name, event.id)
                metrics.incr("enrichment.error", enricher=enricher.name)
        metrics.incr("enrichment.events")
        return event
