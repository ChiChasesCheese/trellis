from __future__ import annotations

from sentinel.collectors.base import Collector

COLLECTORS: dict[str, type[Collector]] = {}


def register_collector(cls: type[Collector]) -> type[Collector]:
    """Class decorator: make a Collector discoverable by its ``source`` name."""
    if cls.source in COLLECTORS:
        raise ValueError(f"duplicate collector source: {cls.source}")
    COLLECTORS[cls.source] = cls
    return cls
