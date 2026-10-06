"""Runs enrichment for one event.

TODO(platform): this should be driven by config, per tenant. For now the three built-in
enrichers are wired in by hand because ``history`` needs ``geo`` to have run first.
"""
from __future__ import annotations

import logging

from sentinel import metrics
from sentinel.config import Settings
from sentinel.db import EventRepository
from sentinel.enrichment.base import EnrichmentContext
from sentinel.enrichment.geo_ip import GeoIpEnricher
from sentinel.enrichment.history import HistoryEnricher
from sentinel.enrichment.threat_intel import ThreatIntelEnricher
from sentinel.models import SecurityEvent

log = logging.getLogger(__name__)


class EnrichmentService:
    def __init__(self, settings: Settings, events: EventRepository):
        self.settings = settings
        self._ctx = EnrichmentContext(settings=settings, events=events)
        self._geo = GeoIpEnricher(settings)
        self._history = HistoryEnricher(settings)
        self._intel = ThreatIntelEnricher(settings)

    def enrich(self, event: SecurityEvent) -> SecurityEvent:
        """Mutates and returns ``event``."""
        if event.src_ip:
            event.enrichment[self._geo.name] = self._geo.enrich(event, self._ctx)
        if event.user:
            # history compares against the geo result, so geo has to be first
            event.enrichment[self._history.name] = self._history.enrich(event, self._ctx)
        if event.src_ip:
            event.enrichment[self._intel.name] = self._intel.enrich(event, self._ctx)
        metrics.incr("enrichment.events")
        return event
