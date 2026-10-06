"""Collector base class: read ``<root>/<source>/*.jsonl`` and normalise each record."""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any, ClassVar

from sentinel import metrics
from sentinel.errors import CollectorError
from sentinel.models import SecurityEvent

log = logging.getLogger(__name__)


class Collector(ABC):
    source: ClassVar[str]

    def __init__(self, root: Path, tenant_id: str):
        self.root = Path(root)
        self.tenant_id = tenant_id

    def records(self) -> Iterator[dict[str, Any]]:
        directory = self.root / self.source
        for path in sorted(directory.glob("*.jsonl")):
            for lineno, line in enumerate(path.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    log.warning("%s:%d: invalid JSON, skipped", path.name, lineno)
                    metrics.incr("collector.bad_record", source=self.source)
                    continue
                if not isinstance(record, dict):
                    metrics.incr("collector.bad_record", source=self.source)
                    continue
                yield record

    @abstractmethod
    def normalize(self, record: dict[str, Any]) -> SecurityEvent | None:
        """Turn one raw record into an event.

        Return ``None`` when the record belongs to another tenant. Raise ``CollectorError``
        (or KeyError/ValueError/TypeError) when the record is malformed.
        """

    def collect(self) -> Iterator[SecurityEvent]:
        for record in self.records():
            try:
                event = self.normalize(record)
            except (CollectorError, KeyError, ValueError, TypeError) as exc:
                log.warning("%s: bad record skipped: %s", self.source, exc)
                metrics.incr("collector.bad_record", source=self.source)
                continue
            if event is None:
                continue
            metrics.incr("collector.events", source=self.source)
            yield event
