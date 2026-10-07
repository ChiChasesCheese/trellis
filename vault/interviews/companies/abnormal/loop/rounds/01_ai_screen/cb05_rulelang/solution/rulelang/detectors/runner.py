"""Runs a tenant's detectors over events, in dependency order."""
from __future__ import annotations

import heapq
import logging

from rulelang import metrics
from rulelang.config import Settings
from rulelang.detectors.base import DETECTORS, Detector, DetectorContext
from rulelang.errors import ConfigError
from rulelang.graph import CommGraph
from rulelang.intel import IntelStore
from rulelang.models import Event, Signal
from rulelang.rules.detector import CustomRuleDetector
from rulelang.store import EventRepository

log = logging.getLogger(__name__)


def _find_cycle(by_name: dict[str, Detector], stuck: set[str]) -> list[str]:
    """One concrete cycle among the detectors Kahn's algorithm could not place."""
    node = min(stuck)
    seen: list[str] = []
    while node not in seen:
        seen.append(node)
        node = min(r for r in by_name[node].requires if r in stuck)
    return seen[seen.index(node) :] + [node]


def order_detectors(detectors: list[Detector]) -> list[Detector]:
    """Topological order (Kahn): every detector comes after the ones it ``requires``.

    Ties keep registration order, so detectors with no dependencies behave exactly as before.
    Unknown names and cycles are configuration errors, reported before any event is processed.
    """
    by_name = {d.name: d for d in detectors}
    index = {d.name: i for i, d in enumerate(detectors)}
    waiting = {d.name: len(d.requires) for d in detectors}
    dependants: dict[str, list[str]] = {d.name: [] for d in detectors}
    for d in detectors:
        for req in d.requires:
            if req not in by_name:
                raise ConfigError(f"detector {d.name!r} requires unknown detector {req!r}")
            dependants[req].append(d.name)

    ready = [(index[n], n) for n, k in waiting.items() if k == 0]
    heapq.heapify(ready)
    ordered: list[Detector] = []
    while ready:
        _, name = heapq.heappop(ready)
        ordered.append(by_name[name])
        for dep in dependants[name]:
            waiting[dep] -= 1
            if waiting[dep] == 0:
                heapq.heappush(ready, (index[dep], dep))
    if len(ordered) < len(detectors):
        stuck = {n for n, k in waiting.items() if k > 0}
        raise ConfigError("detector dependency cycle: " + " -> ".join(_find_cycle(by_name, stuck)))
    return ordered


class DetectorRunner:
    def __init__(self, settings: Settings, graph: CommGraph, events: EventRepository):
        self.settings = settings
        self.graph = graph
        self.events = events
        self.intel = IntelStore(settings.intel)

        self.disabled = set(settings.detectors.disabled)
        unknown = self.disabled - set(DETECTORS)
        if unknown:
            raise ConfigError(f"[detectors] disabled names unknown detectors: {', '.join(sorted(unknown))}")
        custom = [CustomRuleDetector(settings, rule) for rule in settings.rules]
        clash = sorted({d.name for d in custom} & set(DETECTORS))
        if clash:
            raise ConfigError(f"[rules] names clash with built-in detectors: {', '.join(clash)}")
        # Ordered with the disabled ones included: a cycle is a bug whoever switched what off.
        self.detectors: list[Detector] = order_detectors([cls(settings) for cls in DETECTORS.values()] + custom)

    def run(self, event: Event) -> list[Signal]:
        """Evaluate every detector that applies to the event's kind; returns the signals produced."""
        ctx = DetectorContext(self.settings, self.graph, self.events, self.intel)
        produced: list[Signal] = []
        # Detectors whose result cannot be trusted for this event: switched off, crashed, or skipped.
        unavailable = set(self.disabled)
        for detector in self.detectors:
            if detector.name in self.disabled or event.kind not in detector.kinds:
                continue
            missing = [r for r in detector.requires if r in unavailable]
            if missing:
                metrics.incr("detector.skipped", detector=detector.name, missing=missing[0])
                unavailable.add(detector.name)
                continue
            try:
                signal = detector.evaluate(event, ctx)
            except Exception:
                log.exception("detector %s failed on event %s", detector.name, event.id)
                metrics.incr("detector.error", detector=detector.name)
                unavailable.add(detector.name)
                continue
            if signal is not None:
                ctx.signals[detector.name] = signal
                produced.append(signal)
        return produced
