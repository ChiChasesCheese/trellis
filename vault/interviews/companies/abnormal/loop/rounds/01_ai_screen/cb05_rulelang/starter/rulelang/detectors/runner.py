"""Runs a tenant's detectors over events."""
from __future__ import annotations

import logging

from rulelang import metrics
from rulelang.config import Settings
from rulelang.detectors.base import DETECTORS, Detector, DetectorContext
from rulelang.errors import ConfigError
from rulelang.graph import CommGraph
from rulelang.intel import IntelStore
from rulelang.models import Event, Signal
from rulelang.store import EventRepository

log = logging.getLogger(__name__)


class DetectorRunner:
    def __init__(self, settings: Settings, graph: CommGraph, events: EventRepository):
        self.settings = settings
        self.graph = graph
        self.events = events
        self.intel = IntelStore(settings.intel)

        disabled = set(settings.detectors.disabled)
        unknown = disabled - set(DETECTORS)
        if unknown:
            raise ConfigError(f"[detectors] disabled names unknown detectors: {', '.join(sorted(unknown))}")
        self.detectors: list[Detector] = [
            cls(settings) for name, cls in DETECTORS.items() if name not in disabled
        ]

    def run(self, event: Event) -> list[Signal]:
        """Evaluate every detector that applies to the event's kind; returns the signals produced."""
        ctx = DetectorContext(self.settings, self.graph, self.events, self.intel)
        produced: list[Signal] = []
        for detector in self.detectors:
            if event.kind not in detector.kinds:
                continue
            try:
                signal = detector.evaluate(event, ctx)
            except Exception:
                log.exception("detector %s failed on event %s", detector.name, event.id)
                metrics.incr("detector.error", detector=detector.name)
                continue
            if signal is not None:
                ctx.signals[detector.name] = signal
                produced.append(signal)
        return produced
