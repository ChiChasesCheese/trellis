"""The Enricher interface.

An enricher looks at one event and returns a dict of facts about it. The service stores the
result under ``event.enrichment[<enricher name>]``, which is where rules read it from.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar

from sentinel.config import Settings
from sentinel.db import EventRepository
from sentinel.models import SecurityEvent


@dataclass
class EnrichmentContext:
    """What an enricher may use besides the event itself."""

    settings: Settings
    events: EventRepository


class Enricher(ABC):
    #: key under which the result is stored in ``event.enrichment``
    name: ClassVar[str]
    #: names of enrichers whose output this one reads; they must run first
    requires: ClassVar[tuple[str, ...]] = ()

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def enrich(self, event: SecurityEvent, ctx: EnrichmentContext) -> dict[str, Any]:
        """Return facts about ``event``, or ``{}`` when the enricher does not apply."""


#: built-in enrichers by name. Tenant plugins are *not* added here (see enrichment/plugins.py).
ENRICHERS: dict[str, type[Enricher]] = {}


def register_enricher(cls: type[Enricher]) -> type[Enricher]:
    if cls.name in ENRICHERS:
        raise ValueError(f"duplicate enricher name: {cls.name}")
    ENRICHERS[cls.name] = cls
    return cls
