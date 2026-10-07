"""The Detector interface and its registry.

A detector looks at one event and returns a ``Signal`` or ``None``. It may read the signals other
detectors already produced for the *same* event through ``ctx.signals`` (keyed by detector name).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar

from rulelang.config import Settings
from rulelang.graph import CommGraph
from rulelang.intel import IntelStore
from rulelang.models import Event, Severity, Signal
from rulelang.store import EventRepository


@dataclass
class DetectorContext:
    """Everything a detector may read. Built fresh for each event."""

    settings: Settings
    graph: CommGraph
    events: EventRepository
    intel: IntelStore
    signals: dict[str, Signal] = field(default_factory=dict)


class Detector(ABC):
    name: ClassVar[str]
    # Event kinds this detector looks at; the runner never calls it for other kinds.
    kinds: ClassVar[tuple[str, ...]] = ("email",)
    # Names of detectors whose signal this one reads from ``ctx.signals``.
    requires: ClassVar[tuple[str, ...]] = ()

    def __init__(self, settings: Settings):
        self.settings = settings
        self.params: dict[str, Any] = settings.detectors.params.get(self.name, {})

    def param(self, key: str, default: Any) -> Any:
        return self.params.get(key, default)

    def signal(self, event: Event, severity: Severity, summary: str, **evidence: Any) -> Signal:
        return Signal(
            detector=self.name,
            event_id=event.id,
            tenant_id=event.tenant_id,
            severity=severity,
            summary=summary,
            evidence=evidence,
        )

    @abstractmethod
    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        """Return a signal, or ``None`` when the detector does not fire."""


DETECTORS: dict[str, type[Detector]] = {}


def register_detector(cls: type[Detector]) -> type[Detector]:
    """Class decorator: make a Detector available to the runner under ``cls.name``."""
    if cls.name in DETECTORS:
        raise ValueError(f"duplicate detector name: {cls.name}")
    DETECTORS[cls.name] = cls
    return cls


def detector_names() -> list[str]:
    return sorted(DETECTORS)
