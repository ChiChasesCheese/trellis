"""Connector base class and registry.

A connector knows one vendor's audit API: how pages are shaped (`parse_page`) and how one raw
record maps onto our `Event` (`normalize`). Paging, counting and drop accounting live here so
every source behaves the same way. Raw pages are read from `<raw_dir>/<source>/page-NNNN.json`;
the next page's file name is the API's continuation token.
"""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Iterator

from ..config import Config
from ..errors import ConnectorError
from ..events import Event

log = logging.getLogger(__name__)
MAX_PAGES = 1000


@dataclass(frozen=True)
class RawRecord:
    source: str
    payload: dict
    page: str


@dataclass
class ConnectorStats:
    fetched: int = 0
    emitted: int = 0
    dropped: Counter = field(default_factory=Counter)  # reason -> count

    @property
    def dropped_total(self) -> int:
        return sum(self.dropped.values())


class Connector(ABC):
    source: ClassVar[str]

    def __init__(self, root: Path, config: Config) -> None:
        self.root = Path(root)
        self.config = config
        self.stats = ConnectorStats()

    @abstractmethod
    def parse_page(self, payload: dict) -> tuple[list[dict], str | None]:
        """Return (records on this page, continuation token or None)."""

    @abstractmethod
    def normalize(self, raw: RawRecord) -> Event | None:
        """Map one raw record to an Event, or `return self.drop("<reason>")` if we do not model it."""

    def drop(self, reason: str) -> None:
        self.stats.dropped[reason] += 1
        log.debug("%s: dropped record (%s)", self.source, reason)
        return None

    def fetch(self) -> Iterator[RawRecord]:
        pages = sorted(self.root.glob("page-*.json"))
        if not pages:
            return
        token: str | None = pages[0].name
        seen: set[str] = set()
        while token:
            if token in seen or len(seen) >= MAX_PAGES:
                raise ConnectorError(f"{self.source}: paging loop at {token}")
            seen.add(token)
            try:
                payload = json.loads((self.root / token).read_text())
            except (OSError, ValueError) as exc:
                raise ConnectorError(f"{self.source}: cannot read page {token}: {exc}") from exc
            page_name = token
            records, token = self.parse_page(payload)
            for record in records:
                self.stats.fetched += 1
                yield RawRecord(self.source, record, page_name)

    def events(self, since: datetime | None = None) -> Iterator[Event]:
        for raw in self.fetch():
            before = self.stats.dropped_total
            event = self.normalize(raw)
            if event is None:
                if self.stats.dropped_total == before:
                    self.drop("unspecified")
                continue
            if since is not None and event.ts < since:
                continue
            self.stats.emitted += 1
            yield event


_REGISTRY: dict[str, type[Connector]] = {}


def register_connector(cls: type[Connector]) -> type[Connector]:
    if cls.source in _REGISTRY:
        raise ConnectorError(f"duplicate connector for source {cls.source!r}")
    _REGISTRY[cls.source] = cls
    return cls


def registered_connectors() -> dict[str, type[Connector]]:
    return dict(_REGISTRY)
