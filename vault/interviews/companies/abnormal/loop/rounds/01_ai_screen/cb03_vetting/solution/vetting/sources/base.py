from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from vetting.metrics import metrics
from vetting.models import Identity, Kind, Observation

log = logging.getLogger(__name__)

SOURCES: dict[str, type["Source"]] = {}


def register_source(cls: type["Source"]) -> type["Source"]:
    """Class decorator: make the source part of every ingest."""
    if cls.name in SOURCES:
        raise ValueError(f"duplicate source name {cls.name!r}")
    SOURCES[cls.name] = cls
    return cls


@dataclass
class Ingested:
    """What a source produced for one record. ``identity`` is None for records that only add
    observations to an identity another source created (identity-provider sign-ins)."""

    identity: Identity | None
    observations: list[Observation] = field(default_factory=list)


class Source(ABC):
    """Reads one kind of raw data under an ingest root and turns it into identities + observations.

    Conventions (see CONTRIBUTING.md):
    * a record that cannot be identified or dated is a *bad record*: count it, log it, skip it;
    * a missing optional field skips that one observation and is counted, never the whole record;
    * values are stored as submitted, normalization happens where values are compared.
    """

    name: ClassVar[str]

    @abstractmethod
    def load(self, root: Path, tenant_id: str) -> Iterator[Ingested]:
        """Yield one ``Ingested`` per usable record under ``root``."""

    def bad_record(self, reason: str) -> None:
        log.warning("%s: skipping bad record: %s", self.name, reason)
        metrics.incr(f"sources.{self.name}.bad_record")

    def observe(
        self,
        out: list[Observation],
        *,
        identity_id: str,
        tenant_id: str,
        kind: Kind,
        value: str | None,
        ts: datetime,
        path: str,
    ) -> None:
        """Append one observation, or count a missing field when ``value`` is empty."""
        text = value.strip() if isinstance(value, str) else value
        if not text:
            metrics.incr(f"sources.{self.name}.missing.{kind.value}")
            return
        out.append(Observation(identity_id, tenant_id, kind, text, self.name, ts, f"{identity_id}#{path}"))
